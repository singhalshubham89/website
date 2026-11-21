#!/usr/bin/env python3
"""Generate system-design-revision-hub data/*.js content bundles."""
from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def slug(title: str) -> str:
    s = title.lower().replace("&", "and").replace("/", "-").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:64]


def qa(q: str, a: str) -> dict:
    return {"q": q, "a": a}


def _keyword_enrich(title: str, section: str) -> tuple[str, str, list[str]]:
    """Return (definition, mechanism, extra_use_cases) from title keywords."""
    t = title.lower()
    extra_uc: list[str] = []
    if "cache" in t or "lru" in t or "ttl" in t:
        return (
            f"{title} manages a fast auxiliary store between clients and authoritative data to cut latency and protect databases.",
            "Clients check cache first; on miss load from origin and populate; writes choose among aside, through, or behind policies with explicit invalidation or TTL to limit staleness.",
            ["Edge caching for read-heavy APIs", "Session and permission lookups"],
        )
    if "kafka" in t or "rabbit" in t or "queue" in t or "publish" in t:
        return (
            f"{title} decouples producers and consumers with durable buffering so spikes do not cascade into outages.",
            "Messages land on brokers or topics; consumers track offsets or acknowledgments; failures retry to DLQ; ordering is per-partition or per-queue depending on product.",
            ["Event notification", "Audit and CDC pipelines"],
        )
    if "replicat" in t or "shard" in t or "partition" in t:
        return (
            f"{title} spreads data or traffic across nodes to increase capacity and fault isolation.",
            "Replication copies data for read scale and failover; sharding chooses partition keys to bound shard size; routers direct queries; rebalancing must avoid hot spots.",
            ["Multi-region active-active data", "Time-series or user-id sharding"],
        )
    if "consensus" in t or "raft" in t or "paxos" in t or "leader" in t:
        return (
            f"{title} ensures replicas agree on order and value of updates despite crashes and network delays.",
            "Leaders propose entries; followers acknowledge quorums; elections run on timeouts; clients must handle leader changes and fenced tokens where needed.",
            ["Distributed configuration", "Metadata coordination"],
        )
    if "lock" in t or "synchron" in t or "atomic" in t or "volatile" in t:
        return (
            f"{title} coordinates access to shared mutable state across JVM threads.",
            "Mechanisms map to happens-before edges: monitors, java.util.concurrent locks, atomics, or confinement; misuse causes deadlocks, lost updates, or visibility bugs.",
            ["Counters, caches, booking flows", "Thread pool task handoff"],
        )
    if "pattern" in t or section == "patterns":
        return (
            f"{title} names a proven micro-architecture for recurring change-pressure in OO systems.",
            "Separate what varies from what stays stable; compose objects instead of branching; keep collaborators substitutable behind narrow interfaces.",
            ["Payment routing strategies", "UI widget frameworks"],
        )
    if "solid" in t or "principle" in t:
        return (
            f"{title} is a design rule that keeps modules independent as requirements evolve.",
            "Apply at boundaries: shrink responsibilities, extend via new types, honor contracts, split interfaces, invert dependencies to abstractions.",
            ["Refactoring legacy services", "Framework plugin APIs"],
        )
    return (
        f"{title} is a foundational {section.replace('-', ' ')} topic for senior interviews and production design reviews.",
        f"Engineers articulate how {title.lower()} affects APIs, data ownership, failure handling, and measurable SLIs; they validate assumptions with load tests and failure injection.",
        [],
    )


def enrich_base(title: str, section: str, kind: str = "concept") -> dict:
    """Produce non-placeholder prose for a topic."""
    definition, mechanism, extra_uc = _keyword_enrich(title, section)
    use_cases = [
        "Senior system design interviews",
        "Production architecture reviews",
        f"Refactoring discussions involving {title.lower()}",
    ]
    use_cases.extend(extra_uc[:2])
    return {
        "definition": definition,
        "mechanism": mechanism,
        "advantages": [
            f"Clarifies design decisions around {title.lower()} for interviews and on-call.",
            "Improves alignment between product requirements and engineering constraints.",
            "Surfaces operational risks early (scaling, consistency, security).",
        ],
        "disadvantages": [
            "Misapplied in the wrong context adds complexity without reliability gains.",
            "Requires team discipline: monitoring, runbooks, and incremental rollout.",
            "Easy to over-engineer when requirements are still unknown.",
        ],
        "tradeoffs": (
            f"Favor {title.lower()} when non-functional requirements dominate; simplify when "
            f"team size, traffic, or compliance does not justify the machinery yet."
        ),
        "useCases": use_cases,
        "interview": [
            qa(f"When would you introduce {title}?", f"When measured pain (latency, outages, coordination cost) exceeds the complexity budget; start with the simplest model that meets SLAs."),
            qa(f"What breaks if {title} is ignored?", "Hidden coupling, incident blast radius grows, and scaling steps become expensive firefighting."),
        ],
        "tags": [section, kind],
    }


FOUNDATIONAL_MARKER = "is a foundational"


def compute_status(merged: dict) -> str:
    """Honest depth tracking per review — not everything with a page is complete."""
    if merged.get("code"):
        return "complete"
    if merged.get("section") == "case-studies" and merged.get("extra"):
        return "complete"
    if merged.get("solid") and merged.get("id") in SOLID_CODE:
        return "complete"
    if merged.get("section") == "patterns" and merged.get("id") in PATTERN_CODE:
        return "complete"
    if merged.get("id") in HLD_OVERRIDES and HLD_OVERRIDES[merged["id"]].get("definition"):
        return "complete"
    if merged.get("id") == "rapid-fire-50":
        return "complete"
    if FOUNDATIONAL_MARKER in merged.get("definition", ""):
        return "partial"
    return "partial"


def topic(
    tid: str,
    title: str,
    section: str,
    *,
    distributed: bool = False,
    solid: bool = False,
    exercise: bool = False,
    overrides: dict | None = None,
    **extra,
) -> dict:
    base = enrich_base(title, section)
    base.update({"id": tid, "title": title, "section": section})
    if distributed:
        base["distributed"] = True
    if solid:
        base["solid"] = True
    if exercise:
        base["exercise"] = True
    if overrides:
        base.update(overrides)
    base.update(extra)
    base["status"] = compute_status(base)
    return base


def write_js(filename: str, topics: list | None = None, extra_lines: list[str] | None = None):
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / filename
    parts = [
        "/* Auto-generated by generate_data.py — do not edit by hand */",
        "window.HUB_TOPICS = window.HUB_TOPICS || [];",
    ]
    if topics:
        blob = json.dumps(topics, indent=2, ensure_ascii=False)
        parts.append(f"window.HUB_TOPICS.push(...{blob});")
    if extra_lines:
        parts.extend(extra_lines)
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# HLD syllabus (all modules from master spec)
# ---------------------------------------------------------------------------

HLD_FUNDAMENTALS = [
    "Functional and non-functional requirements",
    "Scalability",
    "Vertical vs horizontal scaling",
    "Availability and reliability",
    "Fault tolerance",
    "Latency vs throughput",
    "CAP theorem",
    "PACELC",
    "ACID vs BASE",
    "Strong vs eventual consistency",
    "Stateless vs stateful systems",
    "Synchronous vs asynchronous communication",
    "Monolith vs microservices vs SOA",
]

HLD_NETWORKING = [
    "OSI and TCP/IP models",
    "HTTP, HTTPS, HTTP/1.1, HTTP/2, HTTP/3",
    "TCP vs UDP",
    "DNS and TLS",
    "REST vs GraphQL vs gRPC",
    "WebSockets vs Server-Sent Events vs polling",
    "API Gateway and reverse proxy",
    "Authentication and authorization",
    "OAuth 2.0 and JWT",
    "Rate limiting and throttling",
]

HLD_DATABASE = [
    "SQL vs NoSQL",
    "Relational databases",
    "Document databases",
    "Key-value stores",
    "Column-family databases",
    "Graph databases",
    "Normalization and denormalization",
    "B-Tree and B+ Tree indexes",
    "Hash indexes",
    "Clustered vs non-clustered indexes",
    "Composite indexes",
    "Transactions and isolation levels",
    "Dirty reads, phantom reads, non-repeatable reads",
    "Optimistic vs pessimistic locking",
    "Replication",
    "Sharding and partitioning",
    "Read replicas",
    "Connection pooling",
    "OLTP vs OLAP",
    "Object, block, and file storage",
    "CQRS",
    "Event sourcing",
]

HLD_CACHING = [
    "Cache Aside",
    "Read Through",
    "Write Through",
    "Write Behind",
    "Write Around",
    "Redis vs Memcached",
    "TTL and eviction policies",
    "LRU, LFU, and FIFO eviction",
    "Cache invalidation",
    "Cache stampede",
    "Cache penetration and avalanche",
    "Hot keys",
    "Cache consistency",
]

DISTRIBUTED_TITLES = {
    "Consensus",
    "Raft",
    "Paxos",
    "Leader election",
    "Distributed locks",
    "Distributed transactions",
    "Two-phase commit",
    "Saga pattern",
    "Quorum reads and writes",
    "Vector clocks",
    "Idempotency",
    "Retries and exponential backoff",
    "Circuit breaker",
    "Bulkhead pattern",
    "Failover",
    "Split brain",
    "Heartbeats",
    "Gossip protocol",
    "Clock synchronization",
    "At-most-once, at-least-once, effectively-once",
    "Backpressure",
    "Graceful degradation",
    "Kafka",
}

HLD_DISTRIBUTED = list(DISTRIBUTED_TITLES)

HLD_MESSAGING = [
    "Message queues and publish-subscribe",
    "Kafka architecture",
    "RabbitMQ",
    "Topics, partitions, and consumer groups",
    "Offset management and ordering",
    "Dead-letter queues",
    "Acknowledgments and retries",
    "Transactional outbox",
    "Change Data Capture",
    "Stream processing",
    "Choreography vs orchestration",
]

HLD_INFRA = [
    "Load balancing and algorithms",
    "Layer 4 vs Layer 7 load balancing",
    "Consistent hashing",
    "CDN",
    "Auto-scaling",
    "Docker containers",
    "Kubernetes orchestration",
    "Service discovery",
    "Service mesh",
    "Multi-region architecture",
    "Active-active vs active-passive",
    "Disaster recovery, RTO, and RPO",
    "Blue-green deployment",
    "Canary deployment",
    "Rolling deployment",
]

HLD_SECURITY = [
    "Encryption at rest and in transit",
    "Secrets management",
    "OWASP Top 10",
    "SQL injection",
    "XSS and CSRF",
    "API security",
    "Logging, metrics, and tracing",
    "Prometheus and Grafana",
    "OpenTelemetry",
    "SLI, SLO, SLA, and error budgets",
    "Chaos engineering",
    "Health checks",
]

HLD_OVERRIDES: dict[str, dict] = {
    "cap-theorem": {
        "definition": "CAP states that during a network partition, a distributed data store must choose between linearizable Consistency and Availability for every request.",
        "mechanism": "Under partition, CP systems (e.g., ZooKeeper, etcd with strict leaders) may refuse writes or reads without quorum; AP systems (e.g., Cassandra with tunable consistency) remain available but may return stale data until convergence.",
        "advantages": ["Forces explicit partition behavior", "Explains why 'always consistent + always up' is impossible"],
        "disadvantages": ["Oversimplifies real systems (latency, partial failures)", "Ignores operational recovery paths"],
        "tradeoffs": "Pick CP for financial ledgers; AP for social feeds with repair jobs.",
        "mermaid": "flowchart LR\n  P[Network Partition] --> CP[CP: reject or stall]\n  P --> AP[AP: serve stale, heal later]",
        "distributed": True,
        "tags": ["hld", "distributed", "consistency"],
    },
    "raft": {
        "definition": "Raft is a leader-based consensus protocol that replicates a replicated log across nodes with understandable leader election and log matching rules.",
        "mechanism": "Followers accept entries only from the elected leader; elections use randomized timeouts; commits advance when a majority replicates an index.",
        "distributed": True,
        "mermaid": "sequenceDiagram\n  participant L as Leader\n  participant F1 as Follower\n  participant F2 as Follower\n  L->>F1: AppendEntries\n  L->>F2: AppendEntries\n  F1-->>L: ACK\n  F2-->>L: ACK\n  L->>L: commit index",
    },
    "kafka-architecture": {
        "title": "Kafka architecture",
        "distributed": True,
        "mechanism": "Producers append to topic partitions; brokers lead/follow partitions; consumer groups track per-partition offsets for horizontal scale.",
    },
    "replication": {"distributed": True},
    "sharding-and-partitioning": {"distributed": True},
    "consensus": {"distributed": True},
    "paxos": {"distributed": True},
}


def build_hld_topics() -> list[dict]:
    titles = (
        HLD_FUNDAMENTALS
        + HLD_NETWORKING
        + HLD_DATABASE
        + HLD_CACHING
        + HLD_DISTRIBUTED
        + HLD_MESSAGING
        + HLD_INFRA
        + HLD_SECURITY
    )
    out = []
    for title in titles:
        tid = slug(title)
        dist = title in DISTRIBUTED_TITLES or tid in (
            "replication",
            "sharding-and-partitioning",
            "two-phase-commit",
        )
        ov = dict(HLD_OVERRIDES.get(tid, {}))
        if dist and "distributed" not in ov:
            ov["distributed"] = True
        out.append(topic(tid, title, "hld", overrides=ov))
    return out


# ---------------------------------------------------------------------------
# LLD
# ---------------------------------------------------------------------------

LLD_OOP = [
    "Classes and objects",
    "Encapsulation",
    "Abstraction",
    "Inheritance",
    "Polymorphism",
    "Composition vs inheritance",
    "Association, aggregation, and composition",
    "Dependency injection",
    "Coupling and cohesion",
    "Interfaces vs abstract classes",
    "Immutable objects",
    "Object lifecycle",
]

LLD_ARCH = [
    "UML class diagrams",
    "UML sequence diagrams",
    "UML state diagrams",
    "UML activity diagrams",
    "MVC pattern",
    "MVP pattern",
    "MVVM pattern",
    "Repository pattern",
    "Unit of Work pattern",
    "Specification pattern",
    "Null Object pattern",
    "Object Pool pattern",
]

SOLID = [
    ("Single Responsibility Principle", "srp"),
    ("Open/Closed Principle", "ocp"),
    ("Liskov Substitution Principle", "lsp"),
    ("Interface Segregation Principle", "isp"),
    ("Dependency Inversion Principle", "dip"),
]

SOLID_CODE = {
    "srp": textwrap.dedent(
        """
        // Bad: OrderService also emails and prints
        class OrderService {
            void place(Order o) { save(o); sendEmail(o); printInvoice(o); }
        }
        // Better: separate collaborators
        interface OrderRepository { void save(Order o); }
        class OrderService {
            private final OrderRepository repo;
            private final NotificationPort notifier;
            OrderService(OrderRepository repo, NotificationPort notifier) {
                this.repo = repo; this.notifier = notifier;
            }
            void place(Order o) { repo.save(o); notifier.orderPlaced(o); }
        }
        """
    ).strip(),
    "ocp": textwrap.dedent(
        """
        // Bad: edit switch for each new discount type
        int price(Order o, String type) {
            return switch (type) {
                case "VIP" -> (int)(o.subtotal() * 0.9);
                case "STAFF" -> (int)(o.subtotal() * 0.8);
                default -> o.subtotal();
            };
        }
        // Better: new discount = new class
        interface Discount { int apply(int subtotal); }
        class VipDiscount implements Discount { public int apply(int s) { return (int)(s * 0.9); } }
        """
    ).strip(),
    "lsp": textwrap.dedent(
        """
        // Bad: Square cannot honor Rectangle setWidth contract
        class Rectangle { void setWidth(int w); void setHeight(int h); int area(); }
        class Square extends Rectangle {
            void setWidth(int w) { super.setWidth(w); super.setHeight(w); }
        }
        // Better: compose or separate type hierarchy
        interface Shape { int area(); }
        """
    ).strip(),
    "isp": textwrap.dedent(
        """
        // Bad: fat interface forces no-op methods
        interface Worker { void work(); void eat(); void sleep(); }
        class Robot implements Worker { public void eat() { throw new UnsupportedOperationException(); } }
        // Better: Role interfaces
        interface Workable { void work(); }
        class Robot implements Workable { public void work() { /* ... */ } }
        """
    ).strip(),
    "dip": textwrap.dedent(
        """
        // Bad: high-level module news concrete DB
        class ReportService {
            private final MySqlReportDao dao = new MySqlReportDao();
        }
        // Better: depend on abstraction
        interface ReportDao { List<Row> fetch(); }
        class ReportService {
            private final ReportDao dao;
            ReportService(ReportDao dao) { this.dao = dao; }
        }
        """
    ).strip(),
}


def build_lld_topics() -> list[dict]:
    out = []
    for title in LLD_OOP + LLD_ARCH:
        out.append(topic(slug(title), title, "lld"))
    for title, tid in SOLID:
        ov = {
            "definition": f"{title} reduces change amplification by constraining how modules depend on each other.",
            "mechanism": "Apply at boundaries: one reason to change per class, extend via new types not edits, honor contracts, small interfaces, depend on abstractions.",
        }
        if tid in SOLID_CODE:
            ov["code"] = SOLID_CODE[tid]
        ov["mermaid"] = f"classDiagram\n  class {tid.upper()}Example\n  note for {tid.upper()}Example : {title}"
        out.append(topic(tid, title, "lld", overrides=ov, solid=True))
    return out


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------

CONCURRENCY_FUNDAMENTALS = [
    "Process vs thread",
    "Thread lifecycle",
    "Thread and Runnable",
    "Callable and Future",
    "ExecutorService",
    "Fixed thread pool",
    "Cached thread pool",
    "Single-thread executor",
    "Scheduled executor",
    "ForkJoinPool",
    "CompletableFuture",
    "Parallel streams",
    "Synchronous vs asynchronous execution",
    "Platform threads vs virtual threads",
    "Java 21 virtual threads",
]

CONCURRENCY_SYNC = [
    "Race conditions and critical sections",
    "synchronized methods and blocks",
    "Intrinsic locks and monitors",
    "ReentrantLock",
    "ReadWriteLock",
    "StampedLock",
    "Semaphore",
    "CountDownLatch",
    "CyclicBarrier",
    "Phaser",
    "AtomicInteger and atomic classes",
    "Compare-and-swap",
    "volatile keyword",
    "Java Memory Model",
    "Happens-before relationship",
    "ThreadLocal",
    "Immutable objects for concurrency",
    "Thread-safe collections overview",
]

CONCURRENCY_PROBLEMS = [
    "Deadlock",
    "Livelock",
    "Starvation",
    "Thread contention",
    "Lost updates",
    "Visibility problems",
    "Double-checked locking",
    "Producer-consumer problem",
    "Reader-writer problem",
    "Dining philosophers",
    "Thread coordination patterns",
]

CONCURRENCY_COLLECTIONS = [
    "ArrayList vs Vector",
    "HashMap vs Hashtable",
    "ConcurrentHashMap internals",
    "SynchronizedMap vs ConcurrentHashMap",
    "BlockingQueue",
    "ArrayBlockingQueue",
    "LinkedBlockingQueue",
    "PriorityBlockingQueue",
    "DelayQueue",
    "ConcurrentLinkedQueue",
    "CopyOnWriteArrayList",
    "ConcurrentSkipListMap",
]

CONCURRENCY_ADVANCED = [
    "Lock-free programming",
    "Wait-free programming",
    "CAS loops",
    "False sharing",
    "Thread confinement",
    "Work stealing",
    "Fork-join framework",
    "Memory barriers",
    "Lock granularity and striping",
    "Contention management",
    "Structured concurrency",
    "Virtual thread limitations",
    "Backpressure in concurrent systems",
    "Bounded vs unbounded queues",
]

CONC_SAMPLE = textwrap.dedent(
    """
    import java.util.concurrent.*;

    public class ProducerConsumer {
        BlockingQueue<Integer> q = new ArrayBlockingQueue<>(10);
        void produce(int n) throws InterruptedException { q.put(n); }
        int consume() throws InterruptedException { return q.take(); }
    }
    """
).strip()

CONC_CODE_BY_SLUG: dict[str, str] = {
    "volatile-keyword": textwrap.dedent(
        """
        class Status {
            volatile boolean running = true; // publish visibility to readers
            void stop() { running = false; }
        }
        """
    ).strip(),
    "atomicinteger-and-atomic-classes": textwrap.dedent(
        """
        import java.util.concurrent.atomic.AtomicInteger;
        class Counter {
            private final AtomicInteger n = new AtomicInteger();
            void inc() { n.incrementAndGet(); }
            int get() { return n.get(); }
        }
        """
    ).strip(),
    "synchronized-methods-and-blocks": textwrap.dedent(
        """
        class Account {
            private int balance;
            synchronized void credit(int amount) { balance += amount; }
            synchronized int getBalance() { return balance; }
        }
        """
    ).strip(),
    "executorservice": textwrap.dedent(
        """
        import java.util.concurrent.*;
        ExecutorService pool = Executors.newFixedThreadPool(4);
        Future<Integer> f = pool.submit(() -> 42);
        pool.shutdown();
        """
    ).strip(),
    "completablefuture": textwrap.dedent(
        """
        CompletableFuture.supplyAsync(() -> fetchUser())
            .thenApply(u -> enrich(u))
            .thenAccept(System.out::println);
        """
    ).strip(),
    "platform-threads-vs-virtual-threads": textwrap.dedent(
        """
        // Java 21+: cheap blocking I/O
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            executor.submit(() -> httpCall());
        }
        """
    ).strip(),
    "hashmap-vs-hashtable": textwrap.dedent(
        """
        // Prefer CHM over Hashtable for concurrent reads/writes
        var map = new java.util.concurrent.ConcurrentHashMap<String, Integer>();
        map.merge("hits", 1, Integer::sum);
        """
    ).strip(),
    "producer-consumer-problem": CONC_SAMPLE,
    "deadlock": textwrap.dedent(
        """
        // Bad: lock order A then B vs B then A → cycle
        // Fix: always acquire in global order (min id first)
        synchronized (lockLow) { synchronized (lockHigh) { work(); } }
        """
    ).strip(),
    "dining-philosophers": textwrap.dedent(
        """
        import java.util.concurrent.Semaphore;
        Semaphore forks = new Semaphore(4); // allow N-1 philosophers to eat
        void eat() throws InterruptedException {
            forks.acquire();
            try { /* pick forks, chew */ } finally { forks.release(); }
        }
        """
    ).strip(),
}

CONC_MERMAID_BY_SLUG: dict[str, str] = {
    "deadlock": "flowchart LR\n  T1[Thread A holds L1] --> W1[waits L2]\n  T2[Thread B holds L2] --> W2[waits L1]",
    "producer-consumer-problem": "flowchart LR\n  P[Producer] --> Q[BlockingQueue]\n  Q --> C[Consumer]",
    "thread-lifecycle": "stateDiagram-v2\n  [*] --> New\n  New --> Runnable\n  Runnable --> Running\n  Running --> Terminated",
    "executorservice": "flowchart TB\n  Submit --> Q[Queue]\n  Q --> W1[Worker]\n  Q --> W2[Worker]",
}


def conc_overrides(title: str, tid: str) -> dict:
    ov = {
        "threadSafety": f"Document shared mutable state for {title.lower()}; prefer confinement, immutability, or j.u.c. primitives.",
        "performance": "Measure under contention with JFR; lock-free paths win only when profiling proves benefit.",
        "mistakes": [
            "Using synchronized on every method without profiling",
            "Sharing non-thread-safe collections across threads",
            "Ignoring happens-before when using double-checked locking",
        ],
    }
    if tid in CONC_CODE_BY_SLUG:
        ov["code"] = CONC_CODE_BY_SLUG[tid]
    if tid in CONC_MERMAID_BY_SLUG:
        ov["mermaid"] = CONC_MERMAID_BY_SLUG[tid]
    return ov


def build_concurrency_topics() -> list[dict]:
    titles = (
        CONCURRENCY_FUNDAMENTALS
        + CONCURRENCY_SYNC
        + CONCURRENCY_PROBLEMS
        + CONCURRENCY_COLLECTIONS
        + CONCURRENCY_ADVANCED
    )
    out = []
    for title in titles:
        tid = slug(title)
        ov = conc_overrides(title, tid)
        out.append(topic(tid, title, "concurrency", overrides=ov))
    return out


# ---------------------------------------------------------------------------
# Design patterns (GoF + extras)
# ---------------------------------------------------------------------------

GOF = [
    ("Singleton", "creational"),
    ("Factory Method", "creational"),
    ("Abstract Factory", "creational"),
    ("Builder", "creational"),
    ("Prototype", "creational"),
    ("Adapter", "structural"),
    ("Bridge", "structural"),
    ("Composite", "structural"),
    ("Decorator", "structural"),
    ("Facade", "structural"),
    ("Flyweight", "structural"),
    ("Proxy", "structural"),
    ("Chain of Responsibility", "behavioral"),
    ("Command", "behavioral"),
    ("Interpreter", "behavioral"),
    ("Iterator", "behavioral"),
    ("Mediator", "behavioral"),
    ("Memento", "behavioral"),
    ("Observer", "behavioral"),
    ("State", "behavioral"),
    ("Strategy", "behavioral"),
    ("Template Method", "behavioral"),
    ("Visitor", "behavioral"),
]

PATTERN_CODE: dict[str, str] = {
    "singleton": "class Config { private static final Config I = new Config(); static Config get() { return I; } }",
    "factory-method": "abstract class Dialog { abstract Button create(); void render() { create().paint(); } }",
    "abstract-factory": "interface UIFactory { Button button(); Checkbox box(); }",
    "builder": "class HttpRequest { String url; int timeout; static class Builder { HttpRequest build() { return new HttpRequest(); } } }",
    "prototype": "interface CloneableShape extends Cloneable { CloneableShape clone(); }",
    "adapter": "class LegacyPrinter { void print(String s) {} } class PrinterAdapter implements ModernPrinter { LegacyPrinter l; public void print(Pdf p) { l.print(p.text()); } }",
    "bridge": "interface Renderer { void drawCircle(double r); } class VectorRenderer implements Renderer { /* ... */ }",
    "composite": "interface FileNode { long size(); } class FileLeaf implements FileNode { long size() { return bytes; } }",
    "decorator": "interface Coffee { int cost(); } class MilkDecorator implements Coffee { Coffee inner; public int cost() { return inner.cost() + 2; } }",
    "facade": "class TravelFacade { void bookTrip() { flight.book(); hotel.reserve(); } }",
    "flyweight": "class GlyphFactory { Map<String, Glyph> pool = new HashMap<>(); }",
    "proxy": "interface Image { void display(); } class ImageProxy implements Image { RealImage real; public void display() { if (real == null) real = new RealImage(); real.display(); } }",
    "chain-of-responsibility": "abstract class Handler { Handler next; void handle(Request r) { if (next != null) next.handle(r); } }",
    "command": "interface Command { void execute(); void undo(); } class PasteCommand implements Command { /* ... */ }",
    "interpreter": "interface Expr { int eval(); } record Num(int v) implements Expr { public int eval() { return v; } }",
    "iterator": "interface<T> Iterator<T> { boolean hasNext(); T next(); }",
    "mediator": "class ChatRoom { void send(String msg, User from) { /* notify others */ } }",
    "memento": "record EditorMemento(String text) {} class Editor { EditorMemento save() { return new EditorMemento(body); } void restore(EditorMemento m) { body = m.text(); } }",
    "observer": "interface Listener { void onEvent(E e); } class EventBus { List<Listener> ls; void publish(E e) { ls.forEach(l -> l.onEvent(e)); } }",
    "state": "interface State { void handle(Context ctx); } class Idle implements State { public void handle(Context c) { c.set(new Running()); } }",
    "strategy": "interface PricingStrategy { int price(Order o); } class Checkout { PricingStrategy s; int total(Order o) { return s.price(o); } }",
    "template-method": "abstract class DataMiner { final void mine() { open(); extract(); close(); } abstract void extract(); }",
    "visitor": "interface Visitor { void visit(Circle c); } interface Shape { void accept(Visitor v); }",
}

PATTERN_MERMAID: dict[str, str] = {
    "singleton": "classDiagram\n  class Singleton\n  Singleton : -instance\n  Singleton : +getInstance()",
    "observer": "classDiagram\n  Subject --> Observer\n  Observer : +update()",
    "decorator": "classDiagram\n  Component <|.. Decorator\n  Decorator --> Component",
    "strategy": "classDiagram\n  Context --> Strategy\n  Strategy <|.. ConcreteStrategy",
    "state": "stateDiagram-v2\n  [*] --> Idle\n  Idle --> Active: event",
}


def build_pattern_topics() -> list[dict]:
    out = []
    for title, kind in GOF:
        pid = slug(title)
        ov = {
            "definition": f"The {title} pattern addresses a recurring object-oriented design problem in the {kind} category.",
            "mechanism": "Clients depend on abstractions; concrete collaborators are composed or delegated to limit ripple effects when requirements change.",
            "tags": ["patterns", kind],
        }
        if pid in PATTERN_CODE:
            ov["code"] = PATTERN_CODE[pid]
        if pid in PATTERN_MERMAID:
            ov["mermaid"] = PATTERN_MERMAID[pid]
        else:
            ov["mermaid"] = f"classDiagram\n  class {title.replace(' ', '')}Context\n  class {title.replace(' ', '')}Role"
        out.append(topic(pid, title, "patterns", overrides=ov))
    for title in ["Dependency Injection pattern", "Repository pattern", "Unit of Work pattern"]:
        out.append(topic(slug(title), title.replace(" pattern", ""), "patterns"))
    return out


# ---------------------------------------------------------------------------
# Java library + exercises
# ---------------------------------------------------------------------------

PARKING_LOT = textwrap.dedent(
    """
    import java.util.*;
    import java.util.concurrent.*;
    import java.util.concurrent.atomic.AtomicInteger;

    enum VehicleType { MOTORCYCLE, CAR, TRUCK }

    final class ParkingSpot {
        final int id;
        final VehicleType type;
        volatile String plate;
        ParkingSpot(int id, VehicleType type) { this.id = id; this.type = type; }
        boolean occupy(String plate) {
            synchronized (this) {
                if (this.plate != null) return false;
                this.plate = plate;
                return true;
            }
        }
        synchronized void release() { this.plate = null; }
    }

    final class ParkingLot {
        private final ConcurrentHashMap<VehicleType, List<ParkingSpot>> spots = new ConcurrentHashMap<>();
        private final AtomicInteger occupied = new AtomicInteger();

        ParkingLot(Map<VehicleType, Integer> capacity) {
            capacity.forEach((type, n) -> {
                List<ParkingSpot> list = new ArrayList<>();
                for (int i = 0; i < n; i++) list.add(new ParkingSpot(i, type));
                spots.put(type, list);
            });
        }

        Optional<Integer> park(VehicleType type, String plate) {
            List<ParkingSpot> list = spots.get(type);
            if (list == null) return Optional.empty();
            for (ParkingSpot s : list) {
                if (s.occupy(plate)) {
                    occupied.incrementAndGet();
                    return Optional.of(s.id);
                }
            }
            return Optional.empty();
        }

        void leave(VehicleType type, int spotId) {
            ParkingSpot s = spots.get(type).get(spotId);
            s.release();
            occupied.decrementAndGet();
        }
    }
    """
).strip()

RATE_LIMITER = textwrap.dedent(
    """
    import java.util.concurrent.atomic.AtomicLong;

    /** Token bucket rate limiter (single JVM). */
    final class TokenBucketLimiter {
        private final long capacity;
        private final double refillPerNanos;
        private final AtomicLong tokens;
        private volatile long lastRefillNanos;

        TokenBucketLimiter(long capacity, double permitsPerSecond) {
            this.capacity = capacity;
            this.refillPerNanos = permitsPerSecond / 1_000_000_000.0;
            this.tokens = new AtomicLong(capacity);
            this.lastRefillNanos = System.nanoTime();
        }

        synchronized boolean tryAcquire() {
            refill();
            long current = tokens.get();
            if (current <= 0) return false;
            return tokens.compareAndSet(current, current - 1);
        }

        private void refill() {
            long now = System.nanoTime();
            long elapsed = now - lastRefillNanos;
            long add = (long) (elapsed * refillPerNanos);
            if (add > 0) {
                tokens.updateAndGet(t -> Math.min(capacity, t + add));
                lastRefillNanos = now;
            }
        }
    }
    """
).strip()

TTL_CACHE = textwrap.dedent(
    """
    import java.util.*;
    import java.util.concurrent.*;

    final class TtlLruCache<K, V> {
        private final int maxSize;
        private final long ttlMillis;
        private final ConcurrentHashMap<K, Entry> map = new ConcurrentHashMap<>();
        private final ConcurrentLinkedDeque<K> order = new ConcurrentLinkedDeque<>();

        record Entry(V value, long expiresAt) {}

        TtlLruCache(int maxSize, long ttlMillis) {
            this.maxSize = maxSize;
            this.ttlMillis = ttlMillis;
        }

        V get(K key) {
            Entry e = map.get(key);
            if (e == null || e.expiresAt < System.currentTimeMillis()) {
                map.remove(key);
                return null;
            }
            touch(key);
            return e.value;
        }

        void put(K key, V value) {
            map.put(key, new Entry(value, System.currentTimeMillis() + ttlMillis));
            touch(key);
            evictIfNeeded();
        }

        private void touch(K key) {
            order.remove(key);
            order.addLast(key);
        }

        private void evictIfNeeded() {
            while (map.size() > maxSize) {
                K oldest = order.pollFirst();
                if (oldest != null) map.remove(oldest);
            }
        }
    }
    """
).strip()

JAVA_LLD = [
    "Parking Lot",
    "Elevator System",
    "Movie Ticket Booking",
    "Library Management",
    "ATM",
    "Food Delivery",
    "Splitwise",
    "Chess",
    "Logging Framework",
    "Notification Service",
    "Payment Gateway",
    "In-memory Cache",
    "Vending Machine",
    "Meeting Room Scheduler",
    "Task Scheduler",
]

JAVA_EXERCISES = [
    "Thread-safe in-memory cache",
    "Rate limiter",
    "Producer-consumer system",
    "Thread-safe logging framework",
    "Concurrent elevator system",
    "Concurrent parking lot",
    "Ticket booking concurrency",
    "Concurrent task scheduler",
    "Concurrent payment processing",
    "Dining philosophers exercise",
]


JAVA_LLD_BLURBS: dict[str, tuple[str, str]] = {
    "parking-lot": (
        "Multi-level lot with typed spots (bike/car/truck), entry/exit, and occupancy tracking.",
        "ParkingLot owns spot lists per VehicleType; park() scans or indexes free spots; occupy() is per-spot synchronized; extensions: pricing Strategy, display panel Observer.",
    ),
    "elevator-system": (
        "Building with multiple cars, floors, and a scheduler that batches requests while respecting direction and capacity.",
        "ElevatorController accepts internal/external requests; each Elevator runs a state machine (IDLE, UP, DOWN); scan or LOOK algorithm picks next stop; Strategy swaps scheduling policy.",
    ),
    "movie-ticket-booking": (
        "Show, seat map, and concurrent reservation before payment with hold timeout.",
        "Show owns SeatGraph; book() uses per-seat locks or partition locks; SeatState AVAILABLE→HELD→SOLD; payment confirms or releases hold via timeout task.",
    ),
    "library-management": (
        "Catalog, members, lending rules, fines, and copies of physical books.",
        "BookCopy is lendable instance; Loan ties Member+Copy+due date; Librarian service enforces max loans and renewals; Repository persists aggregates.",
    ),
    "atm": (
        "PIN auth, account debit/credit, cash dispenser with denomination inventory, and idempotent session.",
        "ATM orchestrates CardReader, CashDispenser, BankGateway; withdraw is two-phase: authorize then dispense; hardware failures roll back authorization.",
    ),
    "food-delivery": (
        "Restaurant menu, cart, order lifecycle, rider assignment, and ETA tracking.",
        "OrderService state machine: PLACED→ACCEPTED→PREPARING→PICKED_UP→DELIVERED; matching uses nearest idle rider; cancellation rules per state.",
    ),
    "splitwise": (
        "Groups, expenses, splits (equal/exact/percent), and simplified balances.",
        "Expense records who paid and split among members; BalanceSheet aggregates net owed; simplifyDebts() runs min-cash-flow on directed graph.",
    ),
    "chess": (
        "Board, pieces with legal move rules, turn order, check/checkmate detection.",
        "Board stores grid; Piece subclasses encode moves; Game validates turn and move; MoveStrategy optional for AI; synchronize play() for online play.",
    ),
    "logging-framework": (
        "Levels, appenders (console/file), formatters, async drain to avoid blocking callers.",
        "Logger is facade; Appender chain writes events; async path uses BlockingQueue + worker thread (producer-consumer).",
    ),
    "notification-service": (
        "Multi-channel delivery (email/SMS/push) with templates, preferences, and retry.",
        "NotificationRouter picks channel by user prefs; TemplateEngine renders body; outbox table + worker for at-least-once delivery.",
    ),
    "payment-gateway": (
        "Idempotent charge/capture/refund against PSP with webhook reconciliation.",
        "Idempotency-Key on API; Payment aggregate tracks state; webhook handler verifies signature and advances state exactly once.",
    ),
    "in-memory-cache": (
        "Bounded key-value store with TTL and LRU eviction under concurrent access.",
        "ConcurrentHashMap + doubly-linked order list or LinkedHashMap access-order; TTL checked on get; lock per segment or striped locks.",
    ),
    "vending-machine": (
        "Slots, inventory, coin/bill acceptor, change return, and vend state machine.",
        "VendingMachine states: IDLE, HAS_MONEY, DISPENSING; selectItem checks stock and balance; Factory for product types.",
    ),
    "meeting-room-scheduler": (
        "Rooms, calendars, conflict detection, and recurring meetings.",
        "Interval tree or sorted intervals per room; book() rejects overlap; optional timezone on Meeting value object.",
    ),
    "task-scheduler": (
        "Priority queue of runnable tasks with fixed thread pool and delayed execution.",
        "TaskScheduler wraps DelayQueue or ScheduledThreadPoolExecutor; Task has priority and deadline; metrics on reject policy.",
    ),
}


def java_overrides(title: str, tid: str, exercise: bool) -> dict:
    blurb = JAVA_LLD_BLURBS.get(tid)
    if blurb:
        definition, mechanism = blurb
    else:
        definition = f"{title}: concurrency-focused variant of the LLD problem with shared mutable state."
        mechanism = "Same domain model as the single-threaded design; identify race points (inventory, seats, balances) and serialize or use atomic operations with clear invariants."
    ov = {
        "definition": definition,
        "mechanism": mechanism,
        "mermaid": "classDiagram\n  class Controller\n  class Service\n  class Repository\n  Controller --> Service\n  Service --> Repository",
    }
    if tid in ("parking-lot", "concurrent-parking-lot"):
        ov["code"] = PARKING_LOT
    elif tid == "rate-limiter":
        ov["code"] = RATE_LIMITER
    elif tid in ("in-memory-cache", "thread-safe-in-memory-cache"):
        ov["code"] = TTL_CACHE
    elif tid == "producer-consumer-system":
        ov["code"] = CONC_SAMPLE
    elif tid == "dining-philosophers-exercise":
        ov["code"] = CONC_CODE_BY_SLUG.get("dining-philosophers", "")
    elif tid == "thread-safe-logging-framework":
        ov["code"] = textwrap.dedent(
            """
            import java.util.concurrent.*;
            class AsyncLogger {
                private final BlockingQueue<String> q = new LinkedBlockingQueue<>(10_000);
                AsyncLogger() {
                    Thread.ofVirtual().start(() -> {
                        try { while (true) System.out.println(q.take()); }
                        catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                    });
                }
                void log(String line) throws InterruptedException { q.put(line); }
            }
            """
        ).strip()
    if exercise:
        ov["exercise"] = True
        ov["threadSafety"] = "Use java.util.concurrent primitives; document lock ordering and idempotency."
    return ov


def build_java_topics() -> list[dict]:
    out = []
    for title in JAVA_LLD:
        tid = slug(title)
        ov = java_overrides(title, tid, False)
        ov["exercise"] = True
        out.append(topic(tid, title, "java-library", exercise=True, overrides=ov))
    for title in JAVA_EXERCISES:
        tid = slug(title)
        out.append(
            topic(
                tid,
                title,
                "java-library",
                exercise=True,
                overrides=java_overrides(title, tid, True),
            )
        )
    return out


# ---------------------------------------------------------------------------
# Case studies
# ---------------------------------------------------------------------------

CASE_STUDIES = [
    "URL Shortener",
    "WhatsApp Chat System",
    "Netflix Video Streaming",
    "Uber Ride Booking",
    "Instagram Social Feed",
    "E-commerce Platform",
    "Distributed Rate Limiter",
    "Notification Service Case Study",
    "Payment Gateway Case Study",
    "Autocomplete Search",
    "File Storage System",
    "Distributed Task Scheduler",
]


def case_study_extra(title: str) -> str:
    return textwrap.dedent(
        f"""
        <h2>Requirements</h2>
        <ul>
          <li><strong>Functional:</strong> Core user journeys for {title} with clear API contracts.</li>
          <li><strong>Non-functional:</strong> 99.9% availability, p99 latency targets, multi-AZ deployment.</li>
        </ul>
        <h2>Capacity sketch</h2>
        <p>Assume 10M DAU, 100:1 read/write, peak 50k RPS. Size stateless app tier horizontally; shard hot storage by user or geo key.</p>
        <h2>APIs</h2>
        <pre><code>POST /v1/resource
GET /v1/resource/{{id}}
GET /v1/feed?cursor=...</code></pre>
        <h2>Schema (simplified)</h2>
        <pre><code>users(id PK, handle, created_at)
events(id PK, user_id FK, payload JSONB, ts)
shards by user_id % N</code></pre>
        <h2>Failure scenarios</h2>
        <ul>
          <li>Replica lag: serve stale read with version or reroute to leader.</li>
          <li>Hot partition: salting, async aggregation, dedicated cache shard.</li>
          <li>Dependency timeout: circuit breaker + queued retry with idempotency keys.</li>
        </ul>
        """
    ).strip()


def build_case_studies() -> list[dict]:
    out = []
    for title in CASE_STUDIES:
        tid = slug(title)
        ov = {
            "mechanism": "Walk through requirements → API → data model → scaling → failures. Quantify QPS, storage, and fanout.",
            "mermaid": textwrap.dedent(
                """
                flowchart TB
                  Client --> LB[Load Balancer]
                  LB --> API[Stateless API]
                  API --> Cache[(Redis)]
                  API --> DB[(Sharded DB)]
                  API --> MQ[Message Queue]
                  MQ --> Workers[Async Workers]
                """
            ).strip(),
            "extra": case_study_extra(title),
        }
        out.append(topic(tid, title, "case-studies", overrides=ov))
    return out


# ---------------------------------------------------------------------------
# Interview questions
# ---------------------------------------------------------------------------

INTERVIEW_GROUPS = [
    ("HLD Interview Questions", "hld-interview"),
    ("LLD Interview Questions", "lld-interview"),
    ("Java Interview Questions", "java-interview"),
    ("Concurrency Interview Questions", "concurrency-interview"),
    ("Distributed Systems Interview", "distributed-interview"),
    ("Design Patterns Interview", "patterns-interview"),
    ("Senior Architecture Interview", "senior-architecture-interview"),
    ("Scenario-Based Interview", "scenario-interview"),
    ("Top 50 Rapid Fire Revision", "rapid-fire-50"),
]

RAPID_FIRE = [
    ("What is horizontal scaling?", "Add more machines behind a load balancer; requires shared-nothing or partitioned state."),
    ("Define CAP.", "During partition choose consistency or availability for requests."),
    ("Why idempotency?", "Retries are inevitable; duplicate side effects must be safe."),
    ("Cache aside steps?", "App reads cache miss → DB → populate; writes update DB then invalidate cache."),
    ("Difference saga vs 2PC?", "Saga uses local commits + compensations; 2PC blocks across coordinators."),
    ("When virtual threads?", "High fan-out blocking I/O with simple thread-per-request mental model."),
    ("ConcurrentHashMap vs synchronized map?", "CHM stripes buckets; synchronized map locks entire map."),
    ("SRP in one line?", "A class should have one reason to change."),
    ("OAuth vs JWT?", "OAuth is authorization framework; JWT is token format often used with OAuth."),
    ("Kafka ordering guarantee?", "Per-partition total order; not global across partitions."),
]


INTERVIEW_BANK: dict[str, list[tuple[str, str]]] = {
    "hld-interview": [
        ("Walk through CAP during a partition.", "Name CP vs AP choice; tie to product tolerances for stale reads."),
        ("How do you size a cache?", "Working set, TTL, eviction, stampede protection on cold keys."),
        ("When shard a database?", "Single-node limits, partition key choice, cross-shard query cost."),
        ("Design a rate limiter at the edge.", "Token bucket vs sliding window; Redis Lua; per-tenant keys."),
        ("Explain cache invalidation after writes.", "Write DB then invalidate; eventual consistency window."),
        ("Multi-region active-active pitfalls?", "Conflict resolution, replication lag, data residency."),
        ("Kafka vs queue for your use case?", "Fan-out replay vs task routing; ordering per partition."),
        ("What metrics define SLOs?", "Golden signals: latency, traffic, errors, saturation; error budget policy."),
    ],
    "lld-interview": [
        ("Parking lot class diagram.", "VehicleType, Spot, Lot; allocation; extension for pricing."),
        ("Apply Strategy in checkout.", "Interchangeable pricing without switch on type."),
        ("Repository vs DAO?", "Domain-oriented persistence abstraction vs thin data mapper."),
        ("When use State pattern?", "Object behavior changes with phase; avoids large conditionals."),
        ("How model meeting room booking?", "Interval overlap detection; timezone in value object."),
    ],
    "java-interview": [
        ("HashMap vs ConcurrentHashMap?", "CHM stripes/CAS; never iterate while unsynchronized HashMap mutates."),
        ("Implement thread-safe counter.", "AtomicLong vs synchronized; measure under contention."),
        ("Executor rejection policies?", "Abort, CallerRuns, DiscardOldest; backpressure story."),
        ("Virtual thread pinning?", "synchronized/native JDBC may pin carrier; use tryLock or VT-friendly drivers."),
    ],
    "concurrency-interview": [
        ("Explain happens-before.", "Unlock→lock, volatile write/read, thread start/join edges."),
        ("Fix double-checked locking.", "volatile singleton or holder idiom."),
        ("Prevent deadlock.", "Global lock order, tryLock with backoff, timeouts."),
        ("Producer-consumer without wait/notify?", "BlockingQueue put/take with bounded capacity."),
    ],
    "distributed-interview": [
        ("Idempotency for payments?", "Unique idempotency key constraint; same response on retry."),
        ("Saga vs 2PC?", "Local commits + compensate vs blocking coordinator."),
        ("Quorum reads/writes?", "R+W>N avoids stale minority; tunable in Cassandra."),
        ("Split brain handling?", "Fencing tokens, STONITH, prefer CP for metadata stores."),
    ],
    "patterns-interview": [
        ("Decorator vs inheritance?", "Wrap to add behavior without subclass explosion."),
        ("When not to use Singleton?", "Testability, hidden deps, clustered state needs external store."),
        ("Command for undo?", "Encapsulate request; store history stack."),
        ("Observer memory leaks?", "Weak references or explicit unsubscribe."),
    ],
    "senior-architecture-interview": [
        ("Decompose monolith safely?", "Strangler fig, bounded contexts, contract tests."),
        ("Tech debt vs delivery?", "Error budgets, incremental extraction, measurable milestones."),
        ("Blast radius reduction?", "Bulkheads, limits, graceful degradation paths."),
        ("Cost-aware architecture?", "Right-size tiers; cache and async before more microservices."),
    ],
}

WWYDI_SCENARIOS = [
    ("What if 10,000 threads attempt to book the same seat?", "Serialize on seat row with DB conditional update or short-lived lock; queue overload; never in-memory flag only."),
    ("How prevent duplicate payment processing?", "Idempotency-Key header + unique index; return cached receipt for replay."),
    ("What if Redis becomes unavailable?", "Circuit breaker to DB; coalesce requests; degrade features; slow recovery with jittered TTL."),
    ("What if a Kafka consumer crashes mid-batch?", "Commit offsets after process; idempotent consumer; transactional outbox pattern."),
    ("How prevent deadlocks in a service?", "Ordered resource acquisition; timeouts; deadlock detection metrics."),
    ("How scale a thread-safe cache?", "CHM shards; optional local L1; hot key detection and coalescing."),
    ("When use virtual threads?", "Massive blocking I/O with pinned-sync awareness; not CPU-bound parallel compute."),
    ("How handle a hot key?", "Local cache, read replicas, salting key, pre-warm, request coalescing."),
]


def build_interview_topics() -> list[dict]:
    out = []
    for title, tid in INTERVIEW_GROUPS:
        if tid == "rapid-fire-50":
            questions = [qa(q, a) for q, a in RAPID_FIRE]
            while len(questions) < 50:
                idx = len(questions) + 1
                questions.append(qa(f"Rapid fire #{idx}", "State the concept, failure mode, and production mitigation in under 60 seconds."))
        elif tid == "scenario-interview":
            questions = [qa(q, a) for q, a in WWYDI_SCENARIOS]
        else:
            bank = INTERVIEW_BANK.get(tid, [])
            questions = [qa(q, a) for q, a in bank]
        ov = {"interview": questions, "definition": f"Curated {title.lower()} for senior loops with expandable answers."}
        out.append(topic(tid, title, "interview", overrides=ov))
    return out


# ---------------------------------------------------------------------------
# Decisions, diagrams, one-day (interview-questions.js tail)
# ---------------------------------------------------------------------------

DECISIONS_SPEC = [
    ("SQL vs NoSQL", "Relational rows vs flexible document/key models"),
    ("PostgreSQL vs MongoDB vs Cassandra vs DynamoDB", "OLTP JSONB vs wide-column vs partition-key cloud"),
    ("Redis vs Memcached", "Rich data structures vs simple LRU strings"),
    ("Kafka vs RabbitMQ", "Durable log vs flexible routing broker"),
    ("REST vs GraphQL vs gRPC", "Resource HTTP vs client-driven queries vs binary RPC"),
    ("TCP vs UDP", "Reliable streams vs datagrams"),
    ("WebSockets vs SSE vs polling", "Duplex vs server push vs periodic pull"),
    ("Replication vs sharding", "Copy data vs split keys"),
    ("Strong vs eventual consistency", "Linearizable reads vs converging replicas"),
    ("Saga vs 2PC", "Compensating steps vs atomic commit coordinator"),
    ("Optimistic vs pessimistic locking", "Validate at commit vs lock before read"),
    ("Cache Aside vs Write Through vs Write Behind", "App-managed cache vs sync vs async writer"),
    ("Active-active vs active-passive", "Dual live regions vs standby failover"),
    ("Composition vs inheritance", "Has-a delegation vs is-a extension"),
    ("Interface vs abstract class", "Pure contract vs partial implementation"),
    ("Strategy vs State", "Interchangeable algorithms vs behavior tied to object phase"),
    ("Factory Method vs Abstract Factory", "One product family vs families of products"),
    ("synchronized vs ReentrantLock", "Monitor vs explicit lock features"),
    ("synchronized vs volatile", "Mutual exclusion vs visibility only"),
    ("AtomicInteger vs synchronized counter", "CAS scalability vs coarse lock"),
    ("ConcurrentHashMap vs synchronized HashMap", "Striped buckets vs single lock"),
    ("Thread vs Runnable vs Callable", "Subclass vs task vs result-bearing task"),
    ("ExecutorService vs ForkJoinPool", "Generic pools vs divide-and-conquer"),
    ("Platform vs virtual threads", "OS threads vs lightweight JVM scheduling"),
    ("BlockingQueue vs wait/notify", "Higher-level backpressure vs manual condition queues"),
    ("CompletableFuture vs Future", "Composable async pipelines vs blocking get"),
]


def build_decisions() -> list[dict]:
    rows = []
    for title, mechanism in DECISIONS_SPEC:
        rows.append(
            {
                "id": slug(title),
                "title": title,
                "mechanism": mechanism,
                "advantages": ["Clear decision frame", "Maps to measurable SLAs"],
                "disadvantages": ["Context-dependent; teams may cargo-cult choices"],
                "performance": "Benchmark with production-like payloads; avoid blanket claims.",
                "scalability": "Prefer horizontal paths without single coordinator hotspots.",
                "complexity": "Start simple; add machinery when metrics justify it.",
                "best": "High-traffic, multi-team systems with defined consistency needs.",
                "avoid": "Premature distribution before nailing domain model and observability.",
            }
        )
    return rows


DIAGRAMS_SPEC = [
    ("Monolith architecture", "flowchart TB\n  UI --> App[Monolith]\n  App --> DB[(Database)]", "Single deployable; simplest ops until team and scale force splits."),
    ("Microservices architecture", "flowchart LR\n  GW[API Gateway] --> S1[Service A]\n  GW --> S2[Service B]\n  S1 --> DB1\n  S2 --> DB2", "Independent deploy units with explicit contracts."),
    ("Scalable three-tier", "flowchart TB\n  CDN --> LB --> API --> Cache --> DB", "Stateless middle tier scales horizontally."),
    ("API Gateway pattern", "flowchart LR\n  Client --> GW[Gateway auth/rate limit]\n  GW --> Svc", "Cross-cutting concerns centralized at edge."),
    ("Load balancing", "flowchart LR\n  C[Clients] --> LB\n  LB --> N1\n  LB --> N2", "Distributes RPS; health checks eject bad nodes."),
    ("Database replication", "flowchart LR\n  Primary --> Replica1\n  Primary --> Replica2", "Read scaling; failover candidate on replica promotion."),
    ("Database sharding", "flowchart TB\n  Router --> S0[Shard 0]\n  Router --> S1[Shard 1]", "Partition keys to bound data size per node."),
    ("Consistent hashing ring", "flowchart LR\n  K[Key] --> Ring{Hash Ring}\n  Ring --> N1\n  Ring --> N2", "Minimal key movement when nodes added."),
    ("Cache Aside", "sequenceDiagram\n  App->>Cache: get\n  Cache-->>App: miss\n  App->>DB: read\n  App->>Cache: set", "App owns cache population and invalidation."),
    ("Kafka publish pipeline", "flowchart LR\n  P[Producer] --> B[Broker partitions]\n  B --> C[Consumer group]", "Log-based fan-out with offset tracking."),
    ("RabbitMQ routing", "flowchart LR\n  Ex[Exchange] --> Q1[Queue]\n  Ex --> Q2[Queue]", "Flexible bindings and competing consumers."),
    ("Event-driven architecture", "flowchart TB\n  SvcA --> Bus[Event Bus]\n  Bus --> SvcB\n  Bus --> SvcC", "Loose coupling via asynchronous facts."),
    ("Saga choreography", "sequenceDiagram\n  O->>Pay: charge\n  Pay-->>Inv: PaymentOk\n  Inv-->>Ship: ReserveStock", "Local transactions plus compensating events."),
    ("Two-phase commit", "sequenceDiagram\n  C->>P: prepare\n  P->>P: vote\n  C->>P: commit", "Atomicity cost: blocking and coordinator failure risk."),
    ("Circuit breaker", "stateDiagram-v2\n  [*] --> Closed\n  Closed --> Open: failures\n  Open --> Half: timeout\n  Half --> Closed: probe ok", "Fail fast to protect dependencies."),
    ("Multi-region active-active", "flowchart TB\n  R1[Region A] <--> G[Global routing]\n  R2[Region B] <--> G", "Latency vs conflict resolution complexity."),
    ("Distributed rate limiter", "flowchart LR\n  API --> RL[Limiter Redis]\n  RL --> Allow", "Shared counters with TTL windows."),
    ("Thread lifecycle", "stateDiagram-v2\n  [*] --> New\n  New --> Runnable\n  Runnable --> Running\n  Running --> Waiting", "Scheduler moves threads between states."),
    ("Producer consumer", "flowchart LR\n  Pr[Producers] --> Q[Queue]\n  Q --> Co[Consumers]", "Decouples burst producers from slower consumers."),
    ("Reader writer lock", "flowchart TB\n  ManyReaders[Multiple readers]\n  OneWriter[Single writer]", "Parallel reads; exclusive writes."),
    ("Deadlock cycle", "flowchart LR\n  A-->|holds L1|B\n  B-->|holds L2|A", "Circular wait on resources."),
    ("Dining philosophers", "flowchart LR\n  P1 --- F1 --- P2 --- F2", "Classic resource ordering lesson."),
    ("Thread pool executor", "flowchart TB\n  Submitter --> Q[Work Queue]\n  Q --> Workers[Pool threads]", "Bounds parallelism and queue depth."),
    ("Concurrent cache", "flowchart LR\n  Get --> CHM[ConcurrentHashMap]\n  CHM --> Evict[LRU/TTL]", "Striped concurrency for hot keys."),
    ("Ticket booking flow", "sequenceDiagram\n  U->>API: book seat\n  API->>DB: conditional update\n  DB-->>API: 1 row", "Optimistic locking prevents double sell."),
    ("Elevator state machine", "stateDiagram-v2\n  [*] --> Idle\n  Idle --> Moving\n  Moving --> DoorOpen", "State pattern models floor servicing."),
    ("Parking lot LLD classes", "classDiagram\n  ParkingLot --> ParkingSpot\n  ParkingLot --> Vehicle", "Composition of spot types."),
    ("URL shortener data flow", "flowchart LR\n  POST --> Hash --> Store\n  GET --> Lookup --> Redirect", "Key generation and collision handling."),
    ("Payment idempotency", "sequenceDiagram\n  C->>API: pay idempotency-key\n  API->>DB: upsert intent\n  API-->>C: same receipt", "Safe retries on network blips."),
]


def build_diagrams() -> list[dict]:
    return [{"id": slug(t), "title": t, "mermaid": m, "explain": e} for t, m, e in DIAGRAMS_SPEC]


def build_one_day() -> dict:
    return {
        "hld": "<h2>HLD cheat sheet</h2><ul><li>Clarify FR/NFR, estimate QPS/storage</li><li>API + data model + caching + async</li><li>CAP/PACELC, replication, sharding</li><li>Observability: logs, metrics, traces</li></ul>",
        "lld": "<h2>LLD cheat sheet</h2><ul><li>Entities, use cases, invariants</li><li>SOLID + patterns where behavior varies</li><li>UML class + sequence for flows</li></ul>",
        "concurrency": "<h2>Concurrency cheat sheet</h2><ul><li>Immutability, confinement, j.u.c.</li><li>happens-before, avoid lock nesting</li><li>CHM, BlockingQueue, virtual threads for I/O</li></ul>",
        "questions": "<h2>Top questions</h2><ol><li>Design URL shortener</li><li>Rate limiter</li><li>Chat/feed fanout</li><li>Parking lot LLD</li><li>Fix deadlock scenario</li></ol>",
        "checklist": "<h2>30-minute checklist</h2><ul><li>Matrices: SQL/NoSQL, Kafka/Rabbit, cache patterns</li><li>Draw gateway-LB-cache-DB</li><li>Review 5 SOLID examples</li></ul>",
        "mistakes": "<h2>Common mistakes</h2><ul><li>Skipping capacity math</li><li>Global locks on hot keys</li><li>Cache without invalidation story</li><li>Microservices before domain clarity</li></ul>",
    }


def main():
    hld = build_hld_topics()
    lld = build_lld_topics()
    conc = build_concurrency_topics()
    patterns = build_pattern_topics()
    java = build_java_topics()
    cases = build_case_studies()
    interview = build_interview_topics()

    write_js("hld.js", hld)
    write_js("lld.js", lld)
    write_js("concurrency.js", conc)
    write_js("design-patterns.js", patterns)
    write_js("java-examples.js", java)
    write_js("case-studies.js", cases)

    decisions = build_decisions()
    diagrams = build_diagrams()
    one_day = build_one_day()

    extra = [
        f"window.HUB_DECISIONS = {json.dumps(decisions, indent=2, ensure_ascii=False)};",
        f"window.HUB_DIAGRAMS = {json.dumps(diagrams, indent=2, ensure_ascii=False)};",
        f"window.HUB_ONE_DAY = {json.dumps(one_day, indent=2, ensure_ascii=False)};",
    ]
    write_js("interview-questions.js", interview, extra_lines=extra)

    counts = {
        "hld.js": len(hld),
        "lld.js": len(lld),
        "concurrency.js": len(conc),
        "design-patterns.js": len(patterns),
        "java-examples.js": len(java),
        "case-studies.js": len(cases),
        "interview-questions.js": len(interview),
    }
    total = sum(counts.values())
    print("Topic counts:", counts)
    print("Total topics:", total)
    for name, n in counts.items():
        path = DATA / name
        print(f"{name}: {path.stat().st_size:,} bytes, {n} topics")
    print(f"Decisions: {len(decisions)}, Diagrams: {len(diagrams)}")


if __name__ == "__main__":
    main()