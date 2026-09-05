window.DSA_SECTION_VISUALS = (function () {
  const stroke = "currentColor";
  const accent = "#58a6ff";
  const good = "#3fb950";

  const icons = {
    book: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v18H6.5A2.5 2.5 0 0 1 4 18.5V5.5Z"/><path d="M4 5.5A2.5 2.5 0 0 0 6.5 3H20"/></svg>',
    code: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="m8 8-4 4 4 4"/><path d="m16 8 4 4-4 4"/><path d="M13.5 6 10.5 18"/></svg>',
    syntax: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 10h8M8 14h5"/></svg>',
    array: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="3" y="7" width="4" height="10" rx="1"/><rect x="8" y="7" width="4" height="10" rx="1"/><rect x="13" y="7" width="4" height="10" rx="1"/><rect x="18" y="7" width="3" height="10" rx="1"/></svg>',
    matrix: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 10h16M4 16h16M10 4v16M16 4v16"/></svg>',
    string: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M7 6h10v12H7z"/><path d="M9 10h6M9 14h4"/></svg>',
    map: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 7l4-2 4 2 4-2 4 2v12l-4-2-4 2-4-2-4 2V7z"/><path d="M8 5v12M16 7v12"/></svg>',
    set: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="9" cy="12" r="5"/><circle cx="15.5" cy="12" r="5"/></svg>',
    stack: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="6" y="14" width="12" height="4" rx="1"/><rect x="6" y="9" width="12" height="4" rx="1"/><rect x="6" y="4" width="12" height="4" rx="1"/></svg>',
    queue: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="3" y="8" width="5" height="8" rx="1"/><rect x="9" y="8" width="5" height="8" rx="1"/><path d="M16 12h3m0 0 2-2m-2 2 2 2"/></svg>',
    deque: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="5" y="8" width="14" height="8" rx="2"/><path d="M3 12h2M19 12h2"/></svg>',
    heap: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="12" cy="5" r="2"/><circle cx="7" cy="12" r="2"/><circle cx="17" cy="12" r="2"/><circle cx="4" cy="19" r="2"/><circle cx="12" cy="19" r="2"/><circle cx="20" cy="19" r="2"/><path d="M12 7 7 12m5-5 5 5M7 14l-3 3m13-3 3 3M12 14v3"/></svg>',
    sort: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 18V8M8 18V5M12 18v-6M16 18V3M20 18v-9"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="11" cy="11" r="6"/><path d="m20 20-4-4"/></svg>',
    prefix: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="3" y="9" width="4" height="6" rx="1"/><rect x="8" y="9" width="4" height="6" rx="1"/><rect x="13" y="9" width="4" height="6" rx="1"/><rect x="18" y="9" width="3" height="6" rx="1"/><path d="M3 7h18" stroke-dasharray="3 3"/></svg>',
    window: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="3" y="8" width="18" height="8" rx="2"/><rect x="7" y="8" width="8" height="8" fill="rgba(88,166,255,.15)" stroke="' + accent + '"/></svg>',
    pointers: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 12h16"/><path d="m6 9 0 6M18 9v6" stroke="' + accent + '"/><circle cx="6" cy="12" r="1.8" fill="' + accent + '"/><circle cx="18" cy="12" r="1.8" fill="' + good + '"/></svg>',
    intervals: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M3 14h6V8H3zM9 16h7V6H9zM16 12h5V10h-5z"/></svg>',
    graph: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="5" r="2.5"/><circle cx="7" cy="18" r="2.5"/><circle cx="18" cy="17" r="2.5"/><path d="M8 7.5 16 6.5M8.5 16 16.5 15M7.8 8.2 7.5 15.5M17.8 7.8 17.5 14.5"/></svg>',
    bfs: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="12" cy="5" r="2"/><circle cx="7" cy="12" r="2"/><circle cx="17" cy="12" r="2"/><circle cx="12" cy="19" r="2"/><path d="M12 7 7 12m5-5 5 5M7 14l5 5m5-5 5 5"/></svg>',
    dfs: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="12" cy="4.5" r="2"/><circle cx="6.5" cy="12" r="2"/><circle cx="17.5" cy="12" r="2"/><circle cx="10" cy="19.5" r="2"/><path d="M12 6.5 7 12m5-5.5 5.5 5.5M7.5 13.5 10 17.5"/></svg>',
    topo: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="6" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 12h3m4-6 3 6m-7 0h3"/></svg>',
    dijkstra: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="5" cy="12" r="2.5"/><circle cx="19" cy="12" r="2.5"/><circle cx="12" cy="6" r="2.5"/><path d="M7.2 11.2 10.5 7.5M7.2 12.8 10.5 16.5M13.5 7.5 16.8 11.2M13.5 16.5 16.8 12.8"/></svg>',
    tree: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="12" cy="5" r="2.2"/><circle cx="7" cy="13" r="2.2"/><circle cx="17" cy="13" r="2.2"/><circle cx="5" cy="20" r="2.2"/><circle cx="12" cy="20" r="2.2"/><circle cx="19" cy="20" r="2.2"/><path d="M12 7 7 13m5-6 5 6M7 15l-2 3m7-3 0 3m7-3-2 3"/></svg>',
    list: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="6" cy="12" r="2.5"/><circle cx="12" cy="12" r="2.5"/><circle cx="18" cy="12" r="2.5"/><path d="M8.5 12h1M14.5 12h1"/></svg>',
    cycle: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="12" cy="12" r="7"/><path d="M12 8v4l3 2" stroke="' + accent + '"/></svg>',
    dsu: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><circle cx="6" cy="7" r="2"/><circle cx="18" cy="7" r="2"/><circle cx="12" cy="17" r="2"/><path d="M8 8.5 10.5 15M16 8.5 13.5 15"/></svg>',
    trie: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 18h16"/><path d="M12 4v14"/><path d="M8 10h8M7 14h10"/></svg>',
    dp: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><rect x="14" y="14" width="6" height="6"/><path d="M10 7h4M7 10v4M17 10v4M10 17h4" stroke="' + accent + '"/></svg>',
    knapsack: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M7 8h10l1 12H6l1-12z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/><rect x="8" y="11" width="3" height="3" fill="rgba(63,185,80,.2)" stroke="' + good + '"/><rect x="13" y="13" width="3" height="3"/></svg>',
    backtrack: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M6 18 12 6l6 12"/><path d="M9.5 12H14.5"/><path d="M8 15h8" stroke-dasharray="2 2"/></svg>',
    bits: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M5 8h3v8H5zM10 8h3v8h-3zM16 8h3v8h-3z"/><path d="M6.5 11h0M11.5 13h0M17.5 11h0" stroke-width="3"/></svg>',
    math: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M5 18 9 6l3 8 3-8 4 12"/><path d="M6 14h6"/></svg>',
    table: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M4 10h16M4 14h16M10 5v14M15 5v14"/></svg>',
    pattern: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 7h6v6H4zM14 7h6v6h-6zM9 17h6v4H9z"/></svg>',
    translate: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M5 8h8"/><path d="M9 4v8"/><path d="M6 16c1.5 2 4.5 2 6 0"/><path d="M15 8h4l2 4-2 4h-4"/></svg>',
    warn: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M12 4 3 20h18L12 4z"/><path d="M12 10v4M12 17h.01"/></svg>',
    template: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
    brain: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M8 5c-2 1-3 3-3 5a4 4 0 0 0 2 3.5C6 15 7 17 9 18c1.5 1 3.5 1 5 0 2-1 3-3 3-4.5A4 4 0 0 0 19 10c0-2-1-4-3-5-1.5-1-3.5-1-5 0-1.5-1-3.5-1-5 0z"/></svg>',
    map2: '<svg viewBox="0 0 24 24" fill="none" stroke="' + stroke + '" stroke-width="1.8"><path d="M4 6h16M4 12h10M4 18h14"/><circle cx="18" cy="12" r="2" fill="rgba(88,166,255,.2)" stroke="' + accent + '"/></svg>'
  };

  function frame(name, label, body) {
    return (
      '<svg class="viz viz-' + name + '" viewBox="0 0 440 176" role="img" aria-label="' + label + '">' +
      '<text class="viz-kicker" x="16" y="22">' + label + "</text>" +
      body +
      "</svg>"
    );
  }

  function cell(x, y, n, extra) {
    return (
      '<g class="' + (extra || "") + '">' +
      '<rect class="viz-cell" x="' + x + '" y="' + y + '" width="36" height="36" rx="6"/>' +
      '<text class="viz-num" x="' + (x + 18) + '" y="' + (y + 23) + '" text-anchor="middle">' + n + "</text>" +
      "</g>"
    );
  }

  function node(cx, cy, label, extra) {
    return (
      '<g class="' + (extra || "") + '" transform="translate(' + cx + "," + cy + ')">' +
      '<circle class="viz-node" r="14"/>' +
      '<text class="viz-num" y="4" text-anchor="middle">' + label + "</text>" +
      "</g>"
    );
  }

  const diagrams = {
    array: frame(
      "array",
      "ARRAY · index i walks left → right",
      '<text class="viz-sub" x="16" y="42">Contiguous cells. Access any index in O(1).</text>' +
        cell(70, 78, 4) + cell(114, 78, 8) + cell(158, 78, 1) + cell(202, 78, 9) + cell(246, 78, 3) + cell(290, 78, 7) +
        '<text class="viz-muted" x="88" y="132" text-anchor="middle">0</text>' +
        '<text class="viz-muted" x="132" y="132" text-anchor="middle">1</text>' +
        '<text class="viz-muted" x="176" y="132" text-anchor="middle">2</text>' +
        '<text class="viz-muted" x="220" y="132" text-anchor="middle">3</text>' +
        '<text class="viz-muted" x="264" y="132" text-anchor="middle">4</text>' +
        '<text class="viz-muted" x="308" y="132" text-anchor="middle">5</text>' +
        '<rect class="viz-scan" x="70" y="78" width="36" height="36" rx="6"/>' +
        '<text class="viz-action viz-scan-label" x="88" y="168" text-anchor="middle">i</text>'
    ),
    matrix: frame(
      "matrix",
      "2D GRID · visit row by row",
      '<text class="viz-sub" x="16" y="42">grid[r][c] · nested loops over rows then columns.</text>' +
        cell(140, 58, "a") + cell(184, 58, "b") + cell(228, 58, "c") +
        cell(140, 102, "d") + cell(184, 102, "e") + cell(228, 102, "f") +
        '<rect class="viz-scan" x="140" y="58" width="36" height="36" rx="6"/>'
    ),
    stack: frame(
      "stack",
      "STACK · LIFO  last in, first out",
      '<text class="viz-sub" x="16" y="42">Push and pop happen only at the TOP.</text>' +
        '<rect class="viz-well" x="168" y="56" width="104" height="104" rx="10"/>' +
        '<rect class="viz-plate" x="180" y="126" width="80" height="22" rx="5"/><text class="viz-num" x="220" y="142" text-anchor="middle">1</text>' +
        '<rect class="viz-plate" x="180" y="100" width="80" height="22" rx="5"/><text class="viz-num" x="220" y="116" text-anchor="middle">2</text>' +
        '<g class="viz-moving">' +
        '<rect class="viz-plate viz-plate-on" x="180" y="74" width="80" height="22" rx="5"/>' +
        '<text class="viz-num" x="220" y="90" text-anchor="middle">3</text>' +
        "</g>" +
        '<text class="viz-muted" x="286" y="88">← TOP</text>' +
        '<text class="viz-action viz-push-label" x="64" y="88">PUSH 3</text>' +
        '<text class="viz-action viz-pop-label" x="64" y="88">POP 3</text>'
    ),
    queue: frame(
      "queue",
      "QUEUE · FIFO  first in, first out",
      '<text class="viz-sub" x="16" y="42">Enqueue at BACK. Dequeue from FRONT.</text>' +
        '<text class="viz-label viz-good-fill" x="52" y="92">IN</text>' +
        '<text class="viz-label viz-accent-fill" x="372" y="92">OUT</text>' +
        '<path class="viz-flow" d="M78 86h28"/>' +
        '<path class="viz-flow" d="M330 86h28"/>' +
        '<g class="viz-belt">' +
        cell(112, 68, "A", "viz-item-a") +
        cell(162, 68, "B") +
        cell(212, 68, "C") +
        cell(262, 68, "D", "viz-item-d") +
        "</g>" +
        '<text class="viz-muted" x="130" y="128" text-anchor="middle">front</text>' +
        '<text class="viz-muted" x="280" y="128" text-anchor="middle">back</text>'
    ),
    binarySearch: frame(
      "binarySearch",
      "BINARY SEARCH · halve the range",
      '<text class="viz-sub" x="16" y="42">Compare mid. Keep left half or right half.</text>' +
        cell(48, 78, 1) + cell(92, 78, 3) + cell(136, 78, 4) + cell(180, 78, 7) +
        cell(224, 78, 9) + cell(268, 78, 12) + cell(312, 78, 15) + cell(356, 78, 18) +
        '<rect class="viz-range" x="48" y="74" width="344" height="44" rx="8"/>' +
        '<text class="viz-action viz-mid-label" x="198" y="156" text-anchor="middle">mid?</text>' +
        '<text class="viz-muted viz-lo" x="66" y="156" text-anchor="middle">lo</text>' +
        '<text class="viz-muted viz-hi" x="374" y="156" text-anchor="middle">hi</text>'
    ),
    slidingWindow: frame(
      "slidingWindow",
      "SLIDING WINDOW · move a range",
      '<text class="viz-sub" x="16" y="42">Keep a window of k cells. Slide one step at a time.</text>' +
        cell(48, 82, 2) + cell(92, 82, 1) + cell(136, 82, 5) + cell(180, 82, 3) +
        cell(224, 82, 6) + cell(268, 82, 2) + cell(312, 82, 8) +
        '<rect class="viz-window" x="44" y="76" width="136" height="48" rx="8"/>' +
        '<text class="viz-action viz-window-sum" x="112" y="156" text-anchor="middle">sum = 8</text>'
    ),
    twoPointers: frame(
      "twoPointers",
      "TWO POINTERS · meet in the middle",
      '<text class="viz-sub" x="16" y="42">Left moves right. Right moves left. Stop when they cross.</text>' +
        cell(56, 86, 1) + cell(108, 86, 2) + cell(160, 86, 4) + cell(212, 86, 7) +
        cell(264, 86, 8) + cell(316, 86, 9) +
        '<g class="viz-L"><text class="viz-action" x="74" y="78" text-anchor="middle">L</text><path d="M74 80v6" class="viz-flow"/></g>' +
        '<g class="viz-R"><text class="viz-action viz-good-fill" x="334" y="78" text-anchor="middle">R</text><path d="M334 80v6" class="viz-flow viz-good-stroke"/></g>'
    ),
    bfs: frame(
      "bfs",
      "BFS · visit layer by layer",
      '<text class="viz-sub" x="16" y="42">Use a queue. Finish a level before going deeper.</text>' +
        '<path class="viz-edge" d="M220 70 L160 108 M220 70 L220 108 M220 70 L280 108 M160 122 L130 150 M160 122 L190 150 M280 122 L250 150 M280 122 L310 150"/>' +
        node(220, 70, "0", "viz-n viz-n0") +
        node(160, 108, "1", "viz-n viz-n1") +
        node(220, 108, "1", "viz-n viz-n1") +
        node(280, 108, "1", "viz-n viz-n1") +
        node(130, 150, "2", "viz-n viz-n2") +
        node(190, 150, "2", "viz-n viz-n2") +
        node(250, 150, "2", "viz-n viz-n2") +
        node(310, 150, "2", "viz-n viz-n2") +
        '<text class="viz-action viz-lvl" x="40" y="76">level 0</text>'
    ),
    dfs: frame(
      "dfs",
      "DFS · go deep, then backtrack",
      '<text class="viz-sub" x="16" y="42">Follow one path to the end, then unwind and try the next.</text>' +
        '<path class="viz-edge" d="M220 68 L150 110 M220 68 L290 110 M150 124 L120 154 M150 124 L180 154"/>' +
        '<path class="viz-walk" d="M220 68 L150 110 L120 154"/>' +
        node(220, 68, "A", "viz-n viz-d0") +
        node(150, 110, "B", "viz-n viz-d1") +
        node(290, 110, "C", "viz-n viz-d3") +
        node(120, 154, "D", "viz-n viz-d2") +
        node(180, 154, "E", "viz-n viz-d3")
    ),
    graph: frame(
      "graph",
      "GRAPH · nodes + edges",
      '<text class="viz-sub" x="16" y="42">A walk follows an edge from one vertex to the next.</text>' +
        '<path class="viz-edge" d="M110 110 L200 70 L320 100 L250 148 L110 110"/>' +
        '<circle class="viz-token" r="6" cx="110" cy="110"/>' +
        node(110, 110, "A") +
        node(200, 70, "B") +
        node(320, 100, "C") +
        node(250, 148, "D")
    ),
    tree: frame(
      "tree",
      "TREE · parent → children",
      '<text class="viz-sub" x="16" y="42">One root. Every other node has exactly one parent.</text>' +
        '<path class="viz-edge" d="M220 68 L150 112 M220 68 L290 112 M150 126 L120 156 M150 126 L180 156"/>' +
        node(220, 68, "R", "viz-n viz-t0") +
        node(150, 112, "L", "viz-n viz-t1") +
        node(290, 112, "R", "viz-n viz-t2") +
        node(120, 156, "a", "viz-n viz-t3") +
        node(180, 156, "b", "viz-n viz-t3")
    ),
    linkedList: frame(
      "linkedList",
      "LINKED LIST · follow next",
      '<text class="viz-sub" x="16" y="42">Each node stores a value and a pointer to the next node.</text>' +
        '<path class="viz-edge" d="M118 100h42 M198 100h42 M278 100h42"/>' +
        node(100, 100, "1") +
        node(180, 100, "2") +
        node(260, 100, "3") +
        node(340, 100, "4") +
        '<text class="viz-muted" x="376" y="104">null</text>' +
        '<g class="viz-cursor"><polygon points="100,58 92,72 108,72" class="viz-caret"/><text class="viz-action" x="100" y="50" text-anchor="middle">curr</text></g>'
    ),
    heap: frame(
      "heap",
      "MIN-HEAP · smallest stays on top",
      '<text class="viz-sub" x="16" y="42">Insert at the bottom, then bubble up until order is restored.</text>' +
        '<path class="viz-edge" d="M220 70 L160 114 M220 70 L280 114 M160 128 L130 156 M160 128 L190 156"/>' +
        node(220, 70, "2", "viz-n viz-hroot") +
        node(160, 114, "4", "viz-n") +
        node(280, 114, "7", "viz-n") +
        node(130, 156, "9", "viz-n") +
        '<g class="viz-bubble">' + node(190, 156, "1", "viz-n viz-plate-on") + "</g>"
    ),
    hashmap: frame(
      "hashmap",
      "HASH MAP · key → bucket",
      '<text class="viz-sub" x="16" y="42">hash(key) picks a slot. Lookup is O(1) on average.</text>' +
        '<rect class="viz-key" x="28" y="86" width="86" height="36" rx="8"/>' +
        '<text class="viz-num" x="71" y="109" text-anchor="middle">"cat"</text>' +
        '<path class="viz-flow viz-hash-arrow" d="M120 104h36"/>' +
        '<text class="viz-muted" x="138" y="96" text-anchor="middle">hash</text>' +
        cell(170, 86, 0) + cell(220, 86, 1) + cell(270, 86, 2) + cell(320, 86, 3) +
        '<rect class="viz-hit" x="270" y="86" width="36" height="36" rx="6"/>' +
        '<text class="viz-muted" x="188" y="140" text-anchor="middle">0</text>' +
        '<text class="viz-muted" x="238" y="140" text-anchor="middle">1</text>' +
        '<text class="viz-muted" x="288" y="140" text-anchor="middle">2</text>' +
        '<text class="viz-muted" x="338" y="140" text-anchor="middle">3</text>'
    ),
    dp: frame(
      "dp",
      "DP · fill answers from smaller ones",
      '<text class="viz-sub" x="16" y="42">dp[i] is built from already-solved states to the left.</text>' +
        '<g class="viz-dp0">' + cell(70, 86, 1) + "</g>" +
        '<g class="viz-dp1">' + cell(122, 86, 1) + "</g>" +
        '<g class="viz-dp2">' + cell(174, 86, 2) + "</g>" +
        '<g class="viz-dp3">' + cell(226, 86, 3) + "</g>" +
        '<g class="viz-dp4">' + cell(278, 86, 5) + "</g>" +
        '<g class="viz-dp5">' + cell(330, 86, 8) + "</g>" +
        '<text class="viz-muted" x="88" y="144" text-anchor="middle">0</text>' +
        '<text class="viz-muted" x="140" y="144" text-anchor="middle">1</text>' +
        '<text class="viz-muted" x="192" y="144" text-anchor="middle">2</text>' +
        '<text class="viz-muted" x="244" y="144" text-anchor="middle">3</text>' +
        '<text class="viz-muted" x="296" y="144" text-anchor="middle">4</text>' +
        '<text class="viz-muted" x="348" y="144" text-anchor="middle">5</text>' +
        '<text class="viz-action viz-dp-label" x="220" y="168" text-anchor="middle">Fibonacci table</text>'
    ),
    trie: frame(
      "trie",
      "TRIE · share prefixes",
      '<text class="viz-sub" x="16" y="42">Insert "CAT". Each letter is an edge down the tree.</text>' +
        '<path class="viz-edge" d="M220 68 L220 104 M220 118 L160 148 M220 118 L280 148"/>' +
        node(220, 68, "·", "viz-n viz-tr0") +
        node(220, 104, "C", "viz-n viz-tr1") +
        node(160, 148, "A", "viz-n viz-tr2") +
        node(280, 148, "O", "viz-n") +
        '<text class="viz-action viz-tr-word" x="160" y="172" text-anchor="middle">CAT</text>'
    ),
    prefix: frame(
      "prefix",
      "PREFIX SUM · running total",
      '<text class="viz-sub" x="16" y="42">pref[i] = pref[i-1] + a[i]. Range sum becomes two lookups.</text>' +
        cell(70, 70, 2) + cell(122, 70, 1) + cell(174, 70, 3) + cell(226, 70, 4) + cell(278, 70, 2) +
        '<g class="viz-pref">' +
        cell(70, 118, 2, "viz-p0") +
        cell(122, 118, 3, "viz-p1") +
        cell(174, 118, 6, "viz-p2") +
        cell(226, 118, 10, "viz-p3") +
        cell(278, 118, 12, "viz-p4") +
        "</g>" +
        '<text class="viz-muted" x="40" y="92">a</text>' +
        '<text class="viz-muted" x="40" y="140">pref</text>'
    ),
    sort: frame(
      "sort",
      "SORT · swap until ordered",
      '<text class="viz-sub" x="16" y="42">Compare neighbors and swap when they are out of order.</text>' +
        '<g class="viz-bar viz-b0"><rect x="90" y="110" width="28" height="40" rx="4"/><text class="viz-num" x="104" y="164" text-anchor="middle">4</text></g>' +
        '<g class="viz-bar viz-b1"><rect x="140" y="78" width="28" height="72" rx="4"/><text class="viz-num" x="154" y="164" text-anchor="middle">7</text></g>' +
        '<g class="viz-bar viz-b2"><rect x="190" y="126" width="28" height="24" rx="4"/><text class="viz-num" x="204" y="164" text-anchor="middle">2</text></g>' +
        '<g class="viz-bar viz-b3"><rect x="240" y="94" width="28" height="56" rx="4"/><text class="viz-num" x="254" y="164" text-anchor="middle">5</text></g>' +
        '<g class="viz-bar viz-b4"><rect x="290" y="70" width="28" height="80" rx="4"/><text class="viz-num" x="304" y="164" text-anchor="middle">8</text></g>'
    ),
    dsu: frame(
      "dsu",
      "UNION-FIND · merge groups",
      '<text class="viz-sub" x="16" y="42">Two components become one when you union their roots.</text>' +
        '<circle class="viz-group viz-g1" cx="140" cy="108" r="48"/>' +
        '<circle class="viz-group viz-g2" cx="300" cy="108" r="48"/>' +
        node(120, 96, "A") + node(160, 120, "B") +
        node(280, 96, "C") + node(320, 120, "D") +
        '<path class="viz-merge" d="M180 108h80"/>'
    ),
    bits: frame(
      "bits",
      "BITS · flip one flag",
      '<text class="viz-sub" x="16" y="42">Each bit is an independent on/off switch.</text>' +
        '<g class="viz-bit viz-bit0">' + cell(90, 86, "1") + "</g>" +
        '<g class="viz-bit viz-bit1">' + cell(150, 86, "0") + "</g>" +
        '<g class="viz-bit viz-bit2">' + cell(210, 86, "1") + "</g>" +
        '<g class="viz-bit viz-bit3">' + cell(270, 86, "1") + "</g>" +
        '<text class="viz-muted" x="108" y="144" text-anchor="middle">8</text>' +
        '<text class="viz-muted" x="168" y="144" text-anchor="middle">4</text>' +
        '<text class="viz-muted" x="228" y="144" text-anchor="middle">2</text>' +
        '<text class="viz-muted" x="288" y="144" text-anchor="middle">1</text>' +
        '<text class="viz-action viz-bit-label" x="220" y="168" text-anchor="middle">value = 11 → 15</text>'
    ),
    intervals: frame(
      "intervals",
      "INTERVALS · sort, then merge overlap",
      '<text class="viz-sub" x="16" y="42">If the next start is inside the current end, they merge.</text>' +
        '<rect class="viz-int viz-int1" x="60" y="88" width="140" height="22" rx="6"/>' +
        '<rect class="viz-int viz-int2" x="160" y="120" width="120" height="22" rx="6"/>' +
        '<rect class="viz-int viz-merged" x="60" y="88" width="220" height="54" rx="8"/>' +
        '<text class="viz-muted" x="70" y="80">[1, 4]</text>' +
        '<text class="viz-muted" x="170" y="158">[3, 6]</text>'
    )
  };

  const rules = [
    { match: /import|boilerplate/i, icon: "code" },
    { match: /basic syntax/i, icon: "syntax" },
    { match: /2d array|matrix/i, icon: "matrix", diagram: "matrix" },
    { match: /array/i, icon: "array", diagram: "array" },
    { match: /string/i, icon: "string", diagram: "array" },
    { match: /hashmap|dictionary|prefix sum \+ hashmap/i, icon: "map", diagram: "hashmap" },
    { match: /ordered map/i, icon: "map", diagram: "hashmap" },
    { match: /set|subsets|bitmask/i, icon: "set" },
    { match: /stack/i, icon: "stack", diagram: "stack" },
    { match: /queue|level-order/i, icon: "queue", diagram: "queue" },
    { match: /deque/i, icon: "deque", diagram: "queue" },
    { match: /heap|priority queue|dijkstra/i, icon: "heap", diagram: "heap" },
    { match: /sorting/i, icon: "sort", diagram: "sort" },
    { match: /lower bound|upper bound|binary search on answer/i, icon: "search", diagram: "binarySearch" },
    { match: /binary search/i, icon: "search", diagram: "binarySearch" },
    { match: /prefix sum/i, icon: "prefix", diagram: "prefix" },
    { match: /sliding window/i, icon: "window", diagram: "slidingWindow" },
    { match: /two pointers|fast|slow|cycle/i, icon: "pointers", diagram: "twoPointers" },
    { match: /interval/i, icon: "intervals", diagram: "intervals" },
    { match: /weighted graph|graph representation/i, icon: "graph", diagram: "graph" },
    { match: /topological/i, icon: "topo", diagram: "graph" },
    { match: /bfs/i, icon: "bfs", diagram: "bfs" },
    { match: /dfs/i, icon: "dfs", diagram: "dfs" },
    { match: /tree/i, icon: "tree", diagram: "tree" },
    { match: /linked list|reverse linked/i, icon: "list", diagram: "linkedList" },
    { match: /union find|dsu/i, icon: "dsu", diagram: "dsu" },
    { match: /trie/i, icon: "trie", diagram: "trie" },
    { match: /knapsack|dynamic programming|memoization/i, icon: "dp", diagram: "dp" },
    { match: /backtracking/i, icon: "backtrack", diagram: "dfs" },
    { match: /monotonic/i, icon: "stack", diagram: "stack" },
    { match: /bit manipulation/i, icon: "bits", diagram: "bits" },
    { match: /useful math/i, icon: "math" },
    { match: /complexity master|complexity reasoning/i, icon: "table" },
    { match: /pattern/i, icon: "pattern" },
    { match: /translation/i, icon: "translate" },
    { match: /gotchas/i, icon: "warn" },
    { match: /template/i, icon: "template" },
    { match: /mental map/i, icon: "map2" },
    { match: /recommended usage|master syntax/i, icon: "book" }
  ];

  function resolve(title, sectionId) {
    const text = (title || "") + " " + (sectionId || "").replace(/-/g, " ");
    for (const rule of rules) {
      if (rule.match.test(text)) {
        return {
          icon: icons[rule.icon] || icons.book,
          diagram: rule.diagram ? diagrams[rule.diagram] : null
        };
      }
    }
    return { icon: icons.book, diagram: null };
  }

  return { resolve, icons, diagrams };
})();
