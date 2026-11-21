from datetime import date, timedelta
import json
from pathlib import Path

# Concise definition: each week is a curated, deliberately limited syllabus.
# Dometrain exercise titles are learning targets; headings on providers may change.
W = [
# focus, Dometrain, D exercises, Educative pattern, E examples, core IDs, stretch IDs, Fri, Sat exercise, CounterNet, career
('Big-O + Arrays','D01 Algorithm Complexity; D02 Array Algorithms','Classify Big-O; Has Duplicates (nested loops vs HashSet); Reverse Array; Move Zeroes; Second Largest; Rotate by K','Programming foundations (no pattern yet)','', '1480,88','1929','Functional vs non-functional requirements; monolith vs microservices','Draw Angular → ASP.NET Core → database, annotate request/response','Create C# solution; explain a local TCP client/server experiment',''),
('Hash Maps + Strings','D14 Hash Tables (selective)','Frequency Counter; Group Anagrams; First Non-Repeating Character; understand collisions','Hash Maps','Valid Anagram; Two Sum','217,383','205','Client-server; DNS, TCP, ports and HTTP','Trace one API call using browser devtools or curl; diagram the network hops','Implement TCP listener/client exchanging one framed message',''),
('Two Pointers','D17 Two Pointers','Pair Sum in Sorted Array; Remove Duplicates; Palindrome ignoring punctuation','Two Pointers','Valid Palindrome; Squares of a Sorted Array','392,167','REST API design and HTTP status codes','Design GET/POST/PUT API endpoints for a small task service','Document wire protocol and read/write framing edge cases',''),
('Sliding Window','D18 Sliding Window','Maximum sum window of K; Smallest qualifying subarray; Longest unique substring','Sliding Window','Maximum Average Subarray I; Minimum Size Subarray Sum','1456,1004','Relational data modeling; keys; relationships','Design users/nodes/checks schema and sample SQL queries','Test partial TCP writes/reads and message boundaries',''),
('Stacks + Queues','D05 Stacks; D06 Queues','Array stack; circular queue; Balanced Parentheses; Min Stack','Stacks','Valid Parentheses; Daily Temperatures','496,150','SQL indexes, query plans, transactions','Add an index, compare query plans, explain the write cost','Store multiple simulated node definitions with simple in-memory registry',''),
('Binary Search + Sorting','D08 Searching; D09 Basic Sorting (selective)','Iterative Binary Search; first/last position; insertion sort; sortedness check','Modified Binary Search','Binary Search; Search in Rotated Sorted Array','35,153','ACID, database isolation, concurrent updates','Explain lost updates; model a transaction-safe update','Add connection registration and explicit state changes',''),
('Linked Lists','D03 Singly Linked Lists','Build list; insert; delete; reverse; fast/slow pointers','Fast and Slow Pointers; In-Place Linked List','Linked List Cycle; Reverse Linked List','234,19','OOP, interfaces, composition, SOLID basics','Refactor node registry behind an interface; identify responsibilities','Write tests for node registration, removal and state transitions',''),
('Recursion + Tree DFS','D07 Recursion; D11 Binary Trees','Trace call stack; factorial; recursion base case; DFS traversals','Tree Depth-First Search','Diameter of Binary Tree; Path Sum','100,110','Caching basics: read-through, TTL, invalidation','Propose cached node health lookups; demonstrate staleness','Add a simulated heartbeat and connectivity timestamp',''),
('Tree BFS + BST','D11 Binary Trees; D12 Binary Search Trees','Level order; calculate height; BST search/insert/validate','Tree Breadth-First Search; Tree DFS','Binary Tree Level Order Traversal; Validate BST','199,230','LLD: classes, responsibility and UML','Sketch classes for a job monitor and write minimal C# interfaces','Handle node disconnect / reconnect; test state recovery',''),
('Sorting + Intervals','D10 Merge Sort (selected)','Merge two sorted halves; Merge Sort implementation; compare sorting trade-offs','Intervals','Merge Intervals; Insert Interval','435,452','SOLID, dependency injection, Strategy and Factory','Refactor one tightly coupled component using dependency injection','Introduce cancellation token in monitor loop and tests',''),
('Heaps + Top K','D13 Heaps and Priority Queues','Heap array; insert; extract-min; .NET PriorityQueue; Kth largest','Top K Elements','Top K Frequent Elements; Kth Largest Element in an Array','1046,973','LLD exercise: parking lot requirements and classes','Model vehicle, ticket, spot; implement a bounded parking lot feature','Add bounded monitoring schedule (small worker limit)',''),
('Graph BFS/DFS','D15 Graph Fundamentals','Adjacency list; BFS; DFS; connected components; visited set','Graphs','Number of Islands; Clone Graph','695,841','LLD exercise: elevator controller','Model elevator state, request queue and one testable scheduling rule','Represent simulated nodes and connections as a graph',''),
('Topological Sort','D16 Graph Algorithms (selected)','Topological ordering; cycle detection; shortest path in unweighted graph','Topological Sort','Course Schedule','210,994','HLD: requirements, capacity estimates and API boundaries','Estimate traffic/storage and design a simple monitoring API','Implement BFS path or reachability on topology graph','Capture first STAR story from real work'),
('Disjoint Set Union','Implement DSU in C# (no required Dometrain chapter)','Parent array; path compression; union by rank/size; compare to graph DFS','Union Find','Number of Provinces; Redundant Connection','1319,721','HLD: DNS, load balancing, caching and connection reuse','Explain a 10x traffic increase; locate bottlenecks','Compare graph connectivity using BFS vs DSU in a test','Draft 2 resume achievements with real evidence'),
('Dijkstra + Trie','D16 Weighted Graphs + custom Trie','Dijkstra using PriorityQueue; Trie insert/search/prefix','Graphs; Tries','Network Delay Time; Implement Trie','743,208','HLD: replication, partitioning, storage choices','Draw read-heavy API with replica/cache; discuss consistency','Measure topology lookup and path query costs','Draft a concise SWE resume summary'),
('Subsets + Backtracking','D07 Recursion revisit','Decision tree; subsets; permutations; pruning; backtrack undo','Subsets; Backtracking','Subsets; Permutations','90,39','Queues, background processing, retries and idempotency','Design reliable background jobs with explicit states','Create failure simulation: disconnect midway and log events','Prepare 1 behavioral STAR story'),
('1D DP Basics','D19 Dynamic Programming','Fibonacci recursion; memoization; tabulation; climbing stairs; coin change','Dynamic Programming','Climbing Stairs; Coin Change','198,746','Rate limiting, observability, metrics, logging','Design rate limiter; define latency and failure metrics','Instrument worker count, connection failures and latency','Resume proofread: eliminate inflated ownership claims'),
('1D DP Extensions','D19 DP (selective)','Longest Increasing Subsequence; state definition; complexity','Dynamic Programming','Longest Increasing Subsequence; House Robber','213,740','HLD: URL shortener, API/database/cache','Unseen HLD attempt before reading any case solution','Benchmark baseline with defined repeatable workload','Begin identifying target roles & requirements'),
('2D DP + Knapsack','D19 DP (selective)','Longest Common Subsequence; 0/1 Knapsack; top-down vs bottom-up','Dynamic Programming','Longest Common Subsequence; Partition Equal Subset Sum','494,583','Task scheduler + notifications: trade-offs','Design asynchronous notification pipeline incl. retries','Run bounded concurrency experiment and document results','Finalize first resume and LinkedIn draft'),
('Coding Mocks 1','DSA revision (no new Dometrain)','Unseen timed medium; revise weak patterns and edge cases','Mixed patterns (no solution preview)','Revisit weakest Educative pattern','238,981','HLD case: Newsfeed design','40-minute mock: reads/writes, fanout, caching, bottlenecks','Write README: architecture, setup, limitations','Start 5 targeted applications and 3 outreach attempts'),
('Coding Mocks 2','DSA revision (no new Dometrain)','One 45-min coding mock; one code comprehension exercise','Mixed patterns (no solution preview)','Review only patterns missed during mock','875,139','HLD case: chat/messaging service','Mock: ordering, connections, retries, consistency','Record failure demo and run integration tests','Track response rates; revise technical stories'),
('Coding Mocks 3','DSA revision (no new Dometrain)','Two timed rounds; verbal walkthrough; revise top weaknesses','Mixed patterns (no solution preview)','Do not open solutions until after attempt','560,79','Two unseen design mocks','External review: score requirements, APIs, scaling, failure handling','Polish benchmark writeup, diagrams and tests','Refine application funnel and company-specific prep'),
('Application Sprint 1','Maintain DSA','Two unseen coding exercises, revise trees/graphs/DP','Targeted weaknesses','Use course as reference only','146,208','Mixed LLD/HLD mock','Review mock mistakes; strengthen weak fundamentals','Publish CounterNet repo with accurate feature list','Apply selectively; send 3 personalized referrals'),
('Application Sprint 2','Maintain DSA','One medium under time, one comprehensive mock','Targeted weaknesses','Revisit areas from interviews','128,322','Database + concurrency interview practice','Discuss transaction isolation and idempotency under failures','Enhance tests uncovered by review','Interview follow-ups; refine job search tracker'),
('Application Sprint 3','Maintain DSA','Two company-specific unseen problems; explain test cases','Targeted weaknesses','Avoid memorizing solutions','200,347','HLD/LLD interview practice','Design URL shortener and implement a small C# service object','Publish measured results and architecture decision log','Target applications to roles matching your actual experience'),
('Application Sprint 4','Maintain DSA','One mock round, targeted revisions and code reading','Targeted weaknesses','Review weak patterns','49,56','Systems fundamentals interview recap','Defend concurrency, TCP, HTTP, SQL, caching choices','Record short demo walkthrough + setup notes','Recruiter screens, mock behavioral and offer questions'),
('May Final Review','Maintain DSA','Mixed mock plus reflection on recurring failures','Targeted weaknesses','Revisit weakest pattern','215,300','Mock design and performance diagnosis','Explain design alternatives and failure modes without notes','Freeze scope; fix documentation and reproducibility','Review pipeline and June/July resignation condition: written offer first'),
]

assert len(W)==27, len(W)
PHASES=[('Foundation','Nov 23 – Dec 20',1,4,'foundation'),('Core structures','Dec 21 – Jan 31',5,10,'core'),('Advanced graphs','Feb 1 – Mar 7',11,15,'advanced'),('Backtracking + DP','Mar 8 – Apr 4',16,19,'dp'),('Interview execution','Apr 5 – Apr 25',20,22,'interview'),('Apply + convert','Apr 26 – May 30',23,27,'apply')]
LINKS={
1480:'running-sum-of-1d-array',88:'merge-sorted-array',1929:'concatenation-of-array',217:'contains-duplicate',383:'ransom-note',205:'isomorphic-strings',392:'is-subsequence',167:'two-sum-ii-input-array-is-sorted',1456:'maximum-number-of-vowels-in-a-substring-of-given-length',1004:'max-consecutive-ones-iii',496:'next-greater-element-i',150:'evaluate-reverse-polish-notation',35:'search-insert-position',153:'find-minimum-in-rotated-sorted-array',234:'palindrome-linked-list',19:'remove-nth-node-from-end-of-list',100:'same-tree',110:'balanced-binary-tree',199:'binary-tree-right-side-view',230:'kth-smallest-element-in-a-bst',435:'non-overlapping-intervals',452:'minimum-number-of-arrows-to-burst-balloons',1046:'last-stone-weight',973:'k-closest-points-to-origin',695:'max-area-of-island',841:'keys-and-rooms',210:'course-schedule-ii',994:'rotting-oranges',1319:'number-of-operations-to-make-network-connected',721:'accounts-merge',743:'network-delay-time',208:'implement-trie-prefix-tree',90:'subsets-ii',39:'combination-sum',198:'house-robber',746:'min-cost-climbing-stairs',213:'house-robber-ii',740:'delete-and-earn',494:'target-sum',583:'delete-operation-for-two-strings',238:'product-of-array-except-self',981:'time-based-key-value-store',875:'koko-eating-bananas',139:'word-break',560:'subarray-sum-equals-k',79:'word-search',146:'lru-cache',128:'longest-consecutive-sequence',322:'coin-change',200:'number-of-islands',347:'top-k-frequent-elements',49:'group-anagrams',56:'merge-intervals',215:'kth-largest-element-in-an-array',300:'longest-increasing-subsequence'
}
NAMES={
1480:'Running Sum of 1d Array',88:'Merge Sorted Array',1929:'Concatenation of Array',217:'Contains Duplicate',383:'Ransom Note',205:'Isomorphic Strings',392:'Is Subsequence',167:'Two Sum II',1456:'Maximum Number of Vowels',1004:'Max Consecutive Ones III',496:'Next Greater Element I',150:'Evaluate Reverse Polish Notation',35:'Search Insert Position',153:'Find Minimum in Rotated Sorted Array',234:'Palindrome Linked List',19:'Remove Nth Node from End',100:'Same Tree',110:'Balanced Binary Tree',199:'Binary Tree Right Side View',230:'Kth Smallest in a BST',435:'Non-overlapping Intervals',452:'Minimum Arrows to Burst Balloons',1046:'Last Stone Weight',973:'K Closest Points to Origin',695:'Max Area of Island',841:'Keys and Rooms',210:'Course Schedule II',994:'Rotting Oranges',1319:'Connect Network Operations',721:'Accounts Merge',743:'Network Delay Time',208:'Implement Trie',90:'Subsets II',39:'Combination Sum',198:'House Robber',746:'Min Cost Climbing Stairs',213:'House Robber II',740:'Delete and Earn',494:'Target Sum',583:'Delete Operation for Two Strings',238:'Product of Array Except Self',981:'Time Based Key-Value Store',875:'Koko Eating Bananas',139:'Word Break',560:'Subarray Sum Equals K',79:'Word Search',146:'LRU Cache',128:'Longest Consecutive Sequence',322:'Coin Change',200:'Number of Islands',347:'Top K Frequent Elements',49:'Group Anagrams',56:'Merge Intervals',215:'Kth Largest Element',300:'Longest Increasing Subsequence'
}

def make_tasks(week_num, chapter, exercises, pattern, examples, core, stretch, fri, sat, project, career):
    tasks=[]
    def add(group,label,link=None,optional=False):
        number=len(tasks)+1
        tasks.append({'id':f'w{week_num:02d}-t{number:02d}','group':group,'title':label,'url':link,'optional':optional})
    if chapter.strip(): add('dometrain',f'Study: {chapter}','https://dometrain.com/course/hands-on-data-structures-and-algorithms-in-csharp/')
    for ex in [x.strip() for x in exercises.split(';') if x.strip()]: add('dometrain',ex)
    if pattern and not pattern.lower().startswith('programming foundations'):
        add('educative', f'Open Educative: {pattern}','https://www.educative.io/courses/grokking-coding-interview-in-csharp')
    for ex in [x.strip() for x in examples.split(';') if x.strip()]: add('educative',ex, 'https://www.educative.io/courses/grokking-coding-interview-in-csharp')
    for idx,items in enumerate((core,stretch)):
        for pid in [int(x) for x in items.split(',') if x.strip()]:
            add('practice',f'LC {pid} · {NAMES[pid]}',f'https://leetcode.com/problems/{LINKS[pid]}/',bool(idx))
    add('design',f'Friday learn: {fri}','https://www.educative.io/courses/grokking-system-design-fundamentals' if week_num<=8 else 'https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles' if week_num<=12 else 'https://www.educative.io/courses/grokking-the-system-design-interview')
    add('design',f'Saturday apply: {sat}')
    add('project',f'CounterNet: {project}')
    if career: add('career',career)
    add('review','Sunday: re-solve 2 previous difficult DSA problems without hints')
    add('review','Weekly retrospective: record mistakes and one concept explained aloud')
    return tasks

base=date(2026,11,23)
weeks=[]
for i,w in enumerate(W,1):
    if len(w) == 10:
        w = (*w[:6], "", *w[6:])  # no optional stretch task
    focus,dt,dex,ep,ee,core,stretch,fri,sat,project,career=w
    phase=next(p for p in PHASES if p[2]<=i<=p[3])
    st=base+timedelta(days=7*(i-1))
    en=st+timedelta(days=6)
    weeks.append({'id':f'w{i:02d}','number':i,'start':st.isoformat(),'end':en.isoformat(),
      'focus':focus,'phase':phase[4], 'phase_title':phase[0],
      'dometrain':dt,'educative':ep,'friday':fri,'saturday':sat,'project':project,
      'tasks':make_tasks(i,dt,dex,ep,ee,core,stretch,fri,sat,project,career)})

resources=[
 {'name':'Dometrain DSA in C#','url':'https://dometrain.com/course/hands-on-data-structures-and-algorithms-in-csharp/','kind':'Learn foundations'},
 {'name':'Educative Interview Patterns (C#)','url':'https://www.educative.io/courses/grokking-coding-interview-in-csharp','kind':'Guided patterns'},
 {'name':'LeetCode','url':'https://leetcode.com/problemset/','kind':'Unseen practice'},
 {'name':'Educative System Design Fundamentals','url':'https://www.educative.io/courses/grokking-system-design-fundamentals','kind':'Weeks 1–8'},
 {'name':'Educative Low-Level Design','url':'https://www.educative.io/courses/grokking-the-low-level-design-interview-using-ood-principles','kind':'Weeks 9–12'},
 {'name':'Educative Modern System Design','url':'https://www.educative.io/courses/grokking-the-system-design-interview','kind':'Weeks 13+'},
 {'name':'Microsoft C# Collections','url':'https://learn.microsoft.com/en-us/dotnet/standard/collections/','kind':'Reference'},
 {'name':'Microsoft Async Programming','url':'https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/','kind':'Concurrency'},
 {'name':'OSTEP Operating Systems','url':'https://pages.cs.wisc.edu/~remzi/OSTEP/','kind':'OS reference'},
]
phases=[{'name':x[0],'dates':x[1],'startWeek':x[2],'endWeek':x[3],'id':x[4]} for x in PHASES]
raw={'meta':{'title':'SDE Mission Control','startDate':'2026-11-23','endDate':'2027-05-30','endGoal':'April–May applications; target June–July resignation after written offer','hoursPerWeek':22.5,'language':'C#','version':1},'phases':phases,'weeks':weeks,'resources':resources,
'rhythm':[{'day':'Mon','focus':'Dometrain and DSA foundations','hours':'3h'}, {'day':'Tue','focus':'Educative pattern + implementation','hours':'3h'}, {'day':'Wed','focus':'Independent LeetCode practice','hours':'3h'}, {'day':'Thu','focus':'DSA, mistakes and code reading','hours':'3h'}, {'day':'Fri','focus':'System design theory','hours':'2h'}, {'day':'Sat','focus':'Design practice + CS/networking lab','hours':'4h'}, {'day':'Sun','focus':'DSA revision 2h + CounterNet 2.5h','hours':'4.5h'}],
'checkpoints':[
 {'date':'2026-12-20','label':'Foundations','goal':'Solve basic arrays/hashing/two pointers independently; explain Big O and HTTP request flow'},
 {'date':'2027-01-31','label':'Core DSA','goal':'Binary search without boundary bugs, recursive tree traversals, basic LLD and concurrency vocabulary'},
 {'date':'2027-03-07','label':'Graphs','goal':'Choose BFS/DFS/DSU/topological sort/Dijkstra appropriately; design basic scalable systems'},
 {'date':'2027-04-04','label':'DP + HLD','goal':'Derive DP states and recurrences; discuss failures, concurrency, trade-offs and service architecture'},
 {'date':'2027-04-25','label':'Interview baseline','goal':'Unseen medium in ~35–45 min; coherent 40-min design mock; portfolio MVP and active applications'},
 {'date':'2027-05-30','label':'Application conversion','goal':'Run targeted applications, improve from feedback, maintain mocks, aim for written offer before resignation'}],
 'rules':['DSA without Copilot: clarify → examples → brute force → optimize → C# → dry run → Big-O.','Study the Dometrain foundation, then only selected Educative examples, then separate unseen LeetCode problems.','Record Independent / Hints / Solution Needed. Repeat difficult problems after 2 days, 1 week and 3 weeks.','Friday and Saturday remain system design days. Keep one small lab/design exercise every week.','CounterNet is a scoped systems lab, not a second full-time project. Cut project scope before interview practice.','Targets are readiness indicators, not proof of senior-level production experience.','Prioritize real SWE work achievements and accurate behavioral stories; do not inflate QA work into dev ownership.','Apply from April; resign only after a suitable written offer.']}
path=Path(__file__).resolve().parent/'roadmap.json'
path.write_text(json.dumps(raw,indent=2,ensure_ascii=False),encoding='utf-8')
print('Wrote',len(weeks),'weeks',sum(len(w['tasks']) for w in weeks),'tasks',path.stat().st_size,'bytes')
