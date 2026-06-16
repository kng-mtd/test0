# memo

### sub...

| Type        | Contiguous | Order Matters |
| ----------- | ---------- | ------------- |
| substring   | Yes        | Yes           |
| subsequence | No         | Yes           |
| subset      | No         | No            |

## Question Pattern

### 1. 全探索 (Brute Force)

全ての区間や組み合わせを試す。

```js
for(let i=0;i<n;i++){
    for(let j=i;j<n;j++){
        ...
    }
}
```

- O(n²), O(n³)

- Subarray Sum

### 2. Two Pointers

左右から探索。ソート済み　＞　左右から縮める

```js
let l=0,r=n-1;
while(l<r){
    ...
}
```

- Two Sum II
- Container With Most Water
- Valid Palindrome
- 3Sum

### 3. Sliding Window

連続部分配列を扱う。最長、最短、連続区間

```js
let l=0;

for(let r=0;r<n;r++){
    ...
    while(condition){
        l++;
    }
}
```

- Longest Substring Without Repeating Characters
- Max Consecutive Ones III
- Minimum Size Subarray Sum

### 4. Prefix Sum

区間和を高速化。区間和、部分配列の和

```js
prefix[i + 1] = prefix[i] + nums[i];
```

区間和:

```text
prefix[r+1]-prefix[l]
```

- Range Sum Query
- Subarray Sum Equals K

### 5. Prefix Sum + HashMap

部分配列の個数を数える定番。
条件を満たす部分配列の個数

```js
sum += x;
ans += cnt.get(sum - k) || 0;
cnt.set(sum, (cnt.get(sum) || 0) + 1);
```

- Subarray Sum Equals K
- Binary Subarrays With Sum
- Count Number of Nice Subarrays
- Subarray Sums Divisible by K

### 6. Monotonic Stack

単調増加・単調減少スタック。次に大きい要素、次に小さい要素

```js
while (st.length && nums[st.at(-1)] < nums[i]) {
  st.pop();
}
```

- Daily Temperatures
- Next Greater Element
- Largest Rectangle in Histogram

### 7. Monotonic Queue (Deque)

スライディングウィンドウの最大値・最小値。区間最大、区間最小

- Sliding Window Maximum

### 8. Binary Search

探索空間を半分にする。ソート済み　＞　答えを二分探索

```js
while (l <= r) {
  const m = (l + r) >> 1;
}
```

- Search Insert Position
- Find Peak Element

### 9. Binary Search on Answer

答えそのものを二分探索。最小値、最大値を求める

- Koko Eating Bananas
- Capacity To Ship Packages

### 10. Hash Set / Hash Map

出現確認。存在判定、重複判定、頻度集計

```js
const s = new Set();
```

- Contains Duplicate
- Longest Consecutive Sequence
- Two Sum

### 11. Sorting

並び替えて解く。順序が重要

```js
nums.sort((a, b) => a - b);
```

- Merge Intervals
- 3Sum
- Meeting Rooms

### 12. Greedy

その時点で最善を選ぶ。最適解を構築

- Jump Game
- Gas Station
- Partition Labels

### 13. Dynamic Programming (DP)

過去の結果を利用。i番目までの最適解

- House Robber
- Maximum Subarray
- Coin Change

t

### 14. Heap (Priority Queue)

最大値・最小値を頻繁に取得。Top K、優先順位

- Kth Largest Element
- Top K Frequent Elements

## LeetCodeで頻出の見分け方

| 問題文のキーワード          | 解法候補                    |
| --------------------------- | --------------------------- |
| sorted                      | Two Pointers, Binary Search |
| subarray sum                | Prefix Sum                  |
| count subarrays             | Prefix Sum + HashMap        |
| longest / shortest subarray | Sliding Window              |
| next greater                | Monotonic Stack             |
| window maximum              | Monotonic Queue             |
| top k                       | Heap                        |
| minimum feasible value      | Binary Search on Answer     |
| maximum/minimum ending at i | DP                          |

配列問題では、まず次の順で考えるとかなりの問題を分類できます。

```
連続区間？
↓
Yes → Sliding Window / Prefix Sum

個数を数える？
↓
Yes → Prefix Sum + HashMap

次に大きい・小さい？
↓
Yes → Monotonic Stack

最長・最短？
↓
Yes → Sliding Window

最適解？
↓
Yes → DP or Greedy
```

---

### Count Lowercase

```js
const fn = (s) => {
  let c = Array(26).fill(0);
  for (let i of s) c[i.charCodeAt(0) - 97]++;
  let a = {};
  for (let i = 0; i < 26; i++) {
    if (c[i] > 0) a[String.fromCharCode(i + 97)] = c[i];
  }
  return a;
};
```

---

### TreeNode

#### use function

```js
const TreeNode = (val, left = null, right = null) => ({ val, left, right });

const n = TreeNode(val, left, right);

const n = TreeNode(1, TreeNode(2), TreeNode(3));

const root = TreeNode(1);
root.left = TreeNode(2);
root.right = TreeNode(3);
```

#### use class

```js
class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

const n = new TreeNode(val, left, right);
```

#### array to binary tree, using function

```js
const TreeNode = (val, left = null, right = null) => ({ val, left, right });

const buildTree = (arr) => {
  if (!arr.length) return null;
  const root = TreeNode(arr[0]);
  const queue = [root];
  let i = 1;

  while (queue.length && i < arr.length) {
    const node = queue.shift();
    if (arr[i] != null) {
      node.left = TreeNode(arr[i]);
      queue.push(node.left);
    }
    i++;
    if (i < arr.length && arr[i] != null) {
      node.right = TreeNode(arr[i]);
      queue.push(node.right);
    }
    i++;
  }

  return root;
};

const arr = [0, 1, 2, 3, null, null, 6];
const root = buildTree(arr);

console.log(root);
console.log(JSON.stringify(root, null, 2));
```

or without shift()

```js
const buildTree = (arr) => {
  if (!arr.length) return null;
  const root = TreeNode(arr[0]);
  const queue = [root];
  let head = 0;
  let i = 1;

  while (head < queue.length && i < arr.length) {
    const node = queue[head++];
    if (arr[i] != null) {
      node.left = TreeNode(arr[i]);
      queue.push(node.left);
    }
    i++;
    if (i < arr.length && arr[i] != null) {
      node.right = TreeNode(arr[i]);
      queue.push(node.right);
    }
    i++;
  }

  return root;
};
```

---

### heap class

```js
class Heap {
  constructor(fn1 = (a, b) => a < b) {
    this.data = [];
    this.fn1 = fn1;
  }
  size() {
    return this.data.length;
  }
  isEmpty() {
    return this.data.length == 0;
  }
  top() {
    return this.data[0];
  }
  push(value) {
    const a = this.data;
    a.push(value);
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.fn1(a[p], a[i])) break;
      [a[p], a[i]] = [a[i], a[p]];
      i = p;
    }
  }
  pop() {
    const a = this.data;
    if (a.length == 0) return undefined;
    if (a.length == 1) return a.pop();
    const top = a[0];
    a[0] = a.pop();
    let i = 0;
    while (true) {
      let l = i * 2 + 1;
      let r = i * 2 + 2;
      let id = i;
      if (l < a.length && !this.fn1(a[id], a[l])) id = l;
      if (r < a.length && !this.fn1(a[id], a[r])) id = r;
      if (id == i) break;
      [a[i], a[id]] = [a[id], a[i]];
      i = id;
    }
    return top;
  }
}
```

min heap:

```js
const h = new Heap((a, b) => a < b);

h.push(5);
h.push(2);
h.push(8);

console.log(h.pop()); // 2
```

max heap:

```js
const h = new Heap((a, b) => a > b);

h.push(5);
h.push(2);
h.push(8);

console.log(h.pop()); // 8
```

オブジェクト 1. score 降順、2. name 昇順

```js
const h = new Heap((a, b) => {
  if (a.score !== b.score) return a.score > b.score;
  else return a.name < b.name;
});
```

---

---

---

# Easy Problems

# Javascript

## Create Hello World Function

https://leetcode.com/problems/create-hello-world-function/description/

```js
/**
 * @return {Function}
 */
const createHelloWorld = () => {
  return () => 'Hello World';
};

/**
 * const f = createHelloWorld();
 * f(); // "Hello World"
 */
```

## Counter

https://leetcode.com/problems/counter/description/

```js
/**
 * @param {number} n
 * @return {Function} counter
 */
const createCounter = (n) => () => n++;

/**
 * const counter = createCounter(10)
 * counter() // 10
 * counter() // 11
 * counter() // 12
 */
```

## Counter Ⅱ

https://leetcode.com/problems/counter-ii/description/

```js
/**
 * @param {integer} init
 * @return { increment: Function, decrement: Function, reset: Function }
 */
const createCounter = (init) => {
  let val = init;
  const increment = () => ++val;
  const decrement = () => --val;
  const reset = () => {
    val = init;
    return val;
  };

  return { increment, decrement, reset };
};

/**
 * const counter = createCounter(5)
 * counter.increment(); // 6
 * counter.reset(); // 5
 * counter.decrement(); // 4
 */
```

## Apply Transform Over Each Element In Array

https://leetcode.com/problems/apply-transform-over-each-element-in-array/description/

```js
/**
 * @param {number[]} arr
 * @param {Function} fn
 * @return {number[]}
 */
const map = (arr, fn) => {
  let a = [];
  for (let i = 0; i < arr.length; i++) a[i] = fn(arr[i], i);
  return a;
};
```

## Filter Elements From Array

https://leetcode.com/problems/filter-elements-from-array/description/

```js
/**
 * @param {number[]} arr
 * @param {Function} fn
 * @return {number[]}
 */
const filter = (arr, fn) => {
  let a = [];
  for (let i = 0; i < arr.length; i++) {
    if (fn(arr[i], i)) a.push(arr[i]);
  }
  return a;
};
```

## Array Reduce Transformation

https://leetcode.com/problems/array-reduce-transformation/description/

```js
/**
 * @param {number[]} nums
 * @param {Function} fn
 * @param {number} init
 * @return {number}
 */
const reduce = (nums, fn, init) => {
  let val = init;
  for (let i of nums) val = fn(val, i);
  return val;
};
```

## Function Composition

https://leetcode.com/problems/function-composition/description/

```js
/**
 * @param {Function[]} functions
 * @return {Function}
 */
const compose = (functions) => {
  return (x) => {
    for (let fn of functions.reverse()) x = fn(x);
    return x;
  };
};

/**
 * const fn = compose([x => x + 1, x => 2 * x])
 * fn(4) // 9
 */
```

## Allow One Function Call

https://leetcode.com/problems/allow-one-function-call/description/

```js
/**
 * @param {Function} fn
 * @return {Function}
 */
const once = (fn) => {
  let a = false;
  return (...args) => {
    if (a) return undefined;
    a = true;
    return fn(...args);
  };
};

/**
 * let fn = (a,b,c) => (a + b + c)
 * let onceFn = once(fn)
 *
 * onceFn(1,2,3); // 6
 * onceFn(2,3,6); // returns undefined without calling fn
 */
```

## Sleep

https://leetcode.com/problems/sleep/description/

```js
/**
 * @param {number} millis
 * @return {Promise}
 */
const sleep = (millis) => new Promise((res) => setTimeout(res, millis));

/**
 * let t = Date.now()
 * sleep(100).then(() => console.log(Date.now() - t)) // 100
 */
```

## Promise Time Limit

https://leetcode.com/problems/promise-time-limit/description/

```js
/**
 * @param {Function} fn
 * @param {number} t
 * @return {Function}
 */
const timeLimit =
  (fn, t) =>
  (...args) =>
    Promise.race([fn(...args), new Promise((_, rej) => setTimeout(() => rej('Time Limit Exceeded'), t))]);

/**
 * const limited = timeLimit((t) => new Promise(res => setTimeout(res, t)), 100);
 * limited(150).catch(console.log) // "Time Limit Exceeded" at t=100ms
 */
```

## Chunk Array

https://leetcode.com/problems/chunk-array/description/

```js
/**
 * @param {Array} arr
 * @param {number} size
 * @return {Array}
 */
const chunk = (arr, size) => {
  let a = [];
  while (arr.length > 0) a.push(arr.splice(0, size));
  return a;
};
```

## Array Prototype Last

https://leetcode.com/problems/array-prototype-last/description/

```js
/**
 * @return {null|boolean|number|string|Array|Object}
 */
Array.prototype.last = function () {
  if (this.length == 0) return -1;
  return this.pop();
};

/**
 * const arr = [1, 2, 3];
 * arr.last(); // 3
 */
```

## Array Wrapper

https://leetcode.com/problems/array-wrapper/

```js
/**
 * @param {number[]} nums
 * @return {void}
 */
var ArrayWrapper = function (nums) {
  this.nums = nums;
};

/**
 * @return {number}
 */
ArrayWrapper.prototype.valueOf = function () {
  return this.nums.reduce((a, x) => a + x, 0);
};

/**
 * @return {string}
 */
ArrayWrapper.prototype.toString = function () {
  return '[' + String(this.nums) + ']';
};

/**
 * const obj1 = new ArrayWrapper([1,2]);
 * const obj2 = new ArrayWrapper([3,4]);
 * obj1 + obj2; // 10
 * String(obj1); // "[1,2]"
 * String(obj2); // "[3,4]"
 */
```

## Generate Fibonacci Sequence

https://leetcode.com/problems/generate-fibonacci-sequence/description/

```js
/**
 * @return {Generator<number>}
 */
const fibGenerator = function* () {
  let a = 0,
    b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
};

/**
 * const gen = fibGenerator();
 * gen.next().value; // 0
 * gen.next().value; // 1
 */
```

---

---

---

# Arrays & Hashing

## Concatenation of Array

https://neetcode.io/problems/concatenation-of-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  getConcatenation(nums) {
    return [...nums, ...nums];
  }
}
```

## Contains Duplicate

https://neetcode.io/problems/duplicate-integer/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  hasDuplicate(nums) {
    const s = new Set(nums);
    return nums.length != s.size;
  }
}
```

## Valid Anagram

https://neetcode.io/problems/is-anagram/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {boolean}
   */
  isAnagram(s, t) {
    if (s.length != t.length) return false;
    const c1 = s.split('').sort();
    const c2 = t.split('').sort();

    for (let i = 0; i < s.length; i++) if (c1[i] != c2[i]) return false;
    return true;
  }
}
```

```js
class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {boolean}
   */
  isAnagram(s, t) {
    if (s.length != t.length) return false;
    let c = Array(26).fill(0);
    for (let i of s) c[i.charCodeAt(0) - 97]++;
    for (let i of t) c[i.charCodeAt(0) - 97]--;
    return c.every((x) => x == 0);
  }
}
```

## Replace Elements With Greatest Element On Right Side

https://neetcode.io/problems/replace-elements-with-greatest-element-on-right-side/question

```js
class Solution {
  /**
   * @param {number[]} arr
   * @return {number[]}
   */
  replaceElements(arr) {
    let a = [];
    for (let i = 1; i < arr.length; i++) a.push(Math.max(...arr.slice(i)));
    a.push(-1);
    return a;
  }
}
```

## Is Subsequence

https://neetcode.io/problems/is-subsequence/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {boolean}
   */
  isSubsequence(s, t) {
    if (!s) return true;
    let i1 = 0,
      i2 = 0;
    while (i2 < t.length) {
      if (s[i1] == t[i2]) {
        i1++;
        if (i1 == s.length) return true;
      }
      i2++;
    }
    return false;
  }
}
```

## Score of a String

https://neetcode.io/problems/score-of-a-string/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  scoreOfString(s) {
    let a = 0;
    for (let i = 1; i < s.length; i++) a += Math.abs(s.charCodeAt(i - 1) - s.charCodeAt(i));
    return a;
  }
}
```

## Length Of Last Word

https://neetcode.io/problems/length-of-last-word/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  lengthOfLastWord(s) {
    let i1 = s.length - 1;
    while (i1 > -1) {
      if (s[i1] != ' ') break;
      i1--;
    }
    let i2 = i1 - 1;
    while (i2 > -1) {
      if (s[i2] == ' ') break;
      i2--;
    }
    return i1 - i2;
  }
}
```

## Number of Senior Citizens

https://neetcode.io/problems/number-of-senior-citizens/question

```js
class Solution {
  /**
   * @param {string[]} details
   * @return {number}
   */
  countSeniors(details) {
    let a = 0;
    for (let s of details) {
      if (s.slice(11, 13) > 60) a++;
    }
    return a;
  }
}
```

## Two Sum

https://neetcode.io/problems/two-integer-sum/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number[]}
   */
  twoSum(nums, target) {
    const a = target - Math.min(...nums);
    let b = [];
    for (let i = 0; i < nums.length; i++) if (nums[i] <= a) b.push([nums[i], i]);
    for (let i = 0; i < b.length; i++) {
      for (let j = i + 1; j < b.length; j++) if (b[i][0] + b[j][0] == target) return [b[i][1], b[j][1]];
    }
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number[]}
   */
  twoSum(nums, target) {
    const map = new Map();
    let a;
    for (let i = 0; i < nums.length; i++) {
      a = target - nums[i];
      if (map.has(a)) return [map.get(a), i];
      map.set(nums[i], i);
    }
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number[]}
   */
  twoSum(nums, target) {
    let a = [];
    for (let i = 0; i < nums.length; i++) a.push([nums[i], i]);
    a.sort((x1, x2) => x1[0] - x2[0]);
    let l = 0,
      r = a.length - 1;
    while (l < r) {
      const b = a[l][0] + a[r][0];
      if (b == target) return [a[l][1], a[r][1]];
      [l, r] = b < target ? [l + 1, r] : [l, r - 1];
    }
  }
}
```

## Max Consecutive Ones

https://neetcode.io/problems/max-consecutive-ones/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  findMaxConsecutiveOnes(nums) {
    let a = nums.map(String).join('');
    let b = '';
    while (a.includes(b)) b += '1';
    return b.length - 1;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  findMaxConsecutiveOnes(nums) {
    let a0 = 0,
      a = 0;
    for (let i of nums) {
      a = i ? a + 1 : 0;
      a0 = a > a0 ? a : a0;
    }
    return a0;
  }
}
```

## Longest Common Prefix

https://neetcode.io/problems/longest-common-prefix/question

```js
class Solution {
  /**
   * @param {string[]} strs
   * @return {string}
   */
  longestCommonPrefix(strs) {
    let s = strs[0],
      n = s.length;
    for (let i = 0; i < strs.length; i++) {
      while (s != strs[i].slice(0, n)) {
        n--;
        if (n == 0) return '';
        s = s.slice(0, n);
      }
    }
    return s;
  }
}
```

## String Matching in an Array

https://neetcode.io/problems/string-matching-in-an-array/question

```js
class Solution {
  /**
   * @param {string[]} words
   * @return {string[]}
   */
  stringMatching(words) {
    let a = words.join('-');
    let b = [];
    for (let s of words) {
      if (a.length - a.replaceAll(s, '').length > s.length) b.push(s);
    }
    return b;
  }
}
```

## Pascal's Triangle

https://neetcode.io/problems/pascals-triangle/question

```js
class Solution {
  /**
   * @param {number} numRows
   * @return {number[][]}
   */
  generate(numRows) {
    let a = [[1]];
    for (let i = 1; i < numRows; i++) {
      a[i] = [];
      a[i].push(1);
      for (let j = 0; j < i - 1; j++) a[i].push(a[i - 1][j] + a[i - 1][j + 1]);
      a[i].push(1);
    }
    return a;
  }
}
```

## Remove Element

https://neetcode.io/problems/remove-element/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} val
   * @return {number}
   */
  removeElement(nums, val) {
    let k = 0;
    for (let i = 0; i < nums.length; i++) {
      if (nums[i] != val) nums[k++] = nums[i];
    }
    return k;
  }
}
```

## Unique Email Addresses

https://neetcode.io/problems/unique-email-addresses/question

```js
class Solution {
  /**
   * @param {string[]} emails
   * @return {number}
   */
  numUniqueEmails(emails) {
    let a = new Set();
    for (let s of emails) {
      let [b, c] = s.split('@');
      b = b.split('+')[0].replaceAll('.', '');
      a.add(b + '@' + c);
    }
    return a.size;
  }
}
```

## Isomorphic Strings

https://neetcode.io/problems/isomorphic-strings/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {boolean}
   */
  isIsomorphic(s, t) {
    let a1 = {},
      a2 = {};
    for (let i = 0; i < s.length; i++) {
      a1[s[i]] ??= [];
      a1[s[i]].push(i);
    }
    for (let i = 0; i < t.length; i++) {
      a2[t[i]] ??= [];
      a2[t[i]].push(i);
    }
    return Object.values(a1).sort().join('') == Object.values(a2).sort().join('');
  }
}
```

## Can Place Flowers

https://neetcode.io/problems/can-place-flowers/question

```js
class Solution {
  /**
   * @param {number[]} flowerbed
   * @param {number} n
   * @return {boolean}
   */
  canPlaceFlowers(arr, n) {
    if (!n) return true;
    arr.unshift(0);
    arr.push(0);
    for (let i = 1; i < arr.length - 1; i++) {
      if (arr[i - 1] + arr[i] + arr[i + 1] == 0) {
        n--;
        if (!n) return true;
        i++;
      }
    }
    return false;
  }
}
```

## Majority Element

https://neetcode.io/problems/majority-element/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  majorityElement(nums) {
    let a = {};
    for (let i of nums) {
      a[i] = (a[i] ?? 0) + 1;
      if (a[i] == Math.ceil(nums.length / 2)) return i;
    }
  }
}
```

## Maximum Difference Between Even and Odd Frequency I

https://neetcode.io/problems/maximum-difference-between-even-and-odd-frequency-i/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  maxDifference(s) {
    let a = {};
    for (let i = 0; i < s.length; i++) a[s[i]] = (a[s[i]] ?? 0) + 1;
    const b = Math.max(...Object.values(a).filter((x) => x % 2 != 0));
    const c = Math.min(...Object.values(a).filter((x) => x % 2 == 0));
    return b - c;
  }
}
```

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  maxDifference(s) {
    let a = {};
    for (let i = 0; i < s.length; i++) a[s[i]] = (a[s[i]] ?? 0) + 1;
    let b = 0,
      c = Infinity;
    for (let k in a) {
      if (a[k] % 2) {
        b = a[k] > b ? a[k] : b;
      } else {
        c = a[k] < c ? a[k] : c;
      }
    }
    return b - c;
  }
}
```

## Next Greater Element I

https://neetcode.io/problems/next-greater-element-i/question

```js
class Solution {
  /**
   * @param {number[]} nums1
   * @param {number[]} nums2
   * @return {number[]}
   */
  nextGreaterElement(nums1, nums2) {
    let a = [];
    for (let i = 0; i < nums1.length; i++) {
      a[i] = -1;
      for (let ii of nums2.slice(nums2.indexOf(nums1[i]) + 1)) {
        if (ii > nums1[i]) {
          a[i] = ii;
          break;
        }
      }
    }
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums1
   * @param {number[]} nums2
   * @return {number[]}
   */
  nextGreaterElement(nums1, nums2) {
    const n = nums2.length;
    let a = Array(n).fill(-1),
      b = [];
    for (let i = 0; i < n; i++) {
      while (b.length && nums2[i] > nums2[b.at(-1)]) a[b.pop()] = nums2[i];
      b.push(i);
    }
    const c = {};
    for (let i = 0; i < n; i++) c[nums2[i]] = i;
    return nums1.map((x) => a[c[x]]);
  }
}
```

## Longest Strictly Increasing or Strictly Decreasing Subarray

https://neetcode.io/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  longestMonotonicSubarray(nums) {
    let a0 = 1,
      a1 = 1,
      a2 = 1;
    for (let i = 1; i < nums.length; i++) {
      a1 = nums[i] > nums[i - 1] ? a1 + 1 : 1;
      a2 = nums[i] < nums[i - 1] ? a2 + 1 : 1;
      a0 = Math.max(a0, a1, a2);
    }
    return a0;
  }
}
```

## Maximum Ascending Subarray Sum

https://neetcode.io/problems/maximum-ascending-subarray-sum/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  maxAscendingSum(nums) {
    let a = nums[0],
      a0 = a;
    for (let i = 1; i < nums.length; i++) {
      a = nums[i] > nums[i - 1] ? a + nums[i] : nums[i];
      a0 = a > a0 ? a : a0;
    }
    return a0;
  }
}
```

## Find Pivot Index

https://neetcode.io/problems/find-pivot-index/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  pivotIndex(nums) {
    if (nums.length < 2) return 0;
    let a = nums.slice(1).reduce((a, x) => a + x);
    let b = 0,
      c = 0;
    while (c < nums.length) {
      if (a == b) return c;
      //if(a<b) return -1;
      b += nums[c];
      c++;
      a -= nums[c];
    }
    return -1;
  }
}
```

## Kth Distinct String in an Array

https://neetcode.io/problems/kth-distinct-string-in-an-array/question

```js
class Solution {
  /**
   * @param {string[]} arr
   * @param {number} k
   * @return {string}
   */
  kthDistinct(arr, k) {
    let a = {};
    for (let i = 0; i < arr.length; i++) a[arr[i]] = a[arr[i]] ? Infinity : i + 1;
    const b = Object.entries(a);
    if (b.length < k) return '';
    const c = b.sort((x1, x2) => x1[1] - x2[1])[k - 1];
    if (c[1] == Infinity) return '';
    return c[0];
  }
}
```

```js
class Solution {
  /**
   * @param {string[]} arr
   * @param {number} k
   * @return {string}
   */
  kthDistinct(arr, k) {
    let a = {};
    for (let i of arr) a[i] = (a[i] ?? 0) + 1;
    for (let i of arr) {
      if (a[i] == 1) {
        k--;
        if (k == 0) return i;
      }
    }
    return '';
  }
}
```

## Range Sum Query Immutable

https://neetcode.io/problems/range-sum-query-immutable/question

```js
class NumArray {
  /**
   * @param {number[]} nums
   */
  constructor(nums) {
    this.nums = nums;
  }

  /**
   * @param {number} left
   * @param {number} right
   * @return {number}
   */
  sumRange(left, right) {
    return this.nums.slice(left, right + 1).reduce((a, x) => a + x);
  }
}
```

## Find All Numbers Disappeared in An Array

https://neetcode.io/problems/find-all-numbers-disappeared-in-an-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  findDisappearedNumbers(nums) {
    let a = [];
    let b = new Set(nums);
    for (let i = 1; i <= nums.length; i++) if (!b.has(i)) a.push(i);
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  findDisappearedNumbers(nums) {
    for (let i = 0; i < nums.length; i++) {
      let idx = Math.abs(nums[i]) - 1;
      if (nums[idx] > 0) nums[idx] *= -1;
    }
    let res = [];
    for (let i = 0; i < nums.length; i++) {
      if (nums[i] > 0) res.push(i + 1);
    }
    return res;
  }
}
```

## Find Missing and Repeated Values

https://neetcode.io/problems/find-missing-and-repeated-values/question

```js
class Solution {
  /**
   * @param {number[][]} grid
   * @return {number[]}
   */
  findMissingAndRepeatedValues(grid) {
    let c = grid.flat();
    let d = new Set(c);
    let e = 0;
    for (let i of d) e ^= i;
    let a = e;
    for (let i of c) a ^= i;
    let b = e;
    for (let i = 1; i <= grid.length ** 2; i++) b ^= i;
    return [a, b];
  }
}
```

```js
class Solution {
  /**
   * @param {number[][]} grid
   * @return {number[]}
   */
  findMissingAndRepeatedValues(grid) {
    const n = grid.length,
      n2 = n ** 2;
    let c1 = 0,
      c2 = 0;
    for (let i of grid.flat()) [c1, c2] = [c1 + i, c2 + i ** 2];

    const d1 = (n2 * (n2 + 1)) / 2;
    const d2 = (n2 * (n2 + 1) * (2 * n2 + 1)) / 6;
    const e1 = c1 - d1;
    const e2 = (c2 - d2) / e1;

    return [(e1 + e2) / 2, (e1 + e2) / 2 - e1];
  }
}
```

```js
class Solution {
  /**
   * @param {number[][]} grid
   * @return {number[]}
   */
  findMissingAndRepeatedValues(grid) {
    const n = BigInt(grid.length);
    const n2 = n ** 2n;
    let c1 = 0n,
      c2 = 0n;

    for (let v of grid.flat()) {
      const x = BigInt(v);
      c1 += x;
      c2 += x ** 2n;
    }

    const d1 = (n2 * (n2 + 1n)) / 2n;
    const d2 = (n2 * (n2 + 1n) * (2n * n2 + 1n)) / 6n;
    const e1 = c1 - d1;
    const e2 = (c2 - d2) / e1;

    return [Number((e1 + e2) / 2n), Number((e1 + e2) / 2n - e1)];
  }
}
```

## Maximum Number of Balloons

https://neetcode.io/problems/maximum-number-of-balloons/question

```js
class Solution {
  /**
   * @param {string} text
   * @return {number}
   */
  maxNumberOfBalloons(text) {
    let a = {};
    for (let i of text) a[i] = (a[i] ?? 0) + 1;
    return Math.min(a.b, a.a, a.l >> 1, a.o >> 1, a.n) || 0;
  }
}
```

```js
class Solution {
  /**
   * @param {string} text
   * @return {number}
   */
  maxNumberOfBalloons(text) {
    let b = 0,
      a = 0,
      l = 0,
      o = 0,
      n = 0;
    for (let i of text) {
      if (i == 'b') b++;
      else if (i == 'a') a++;
      else if (i == 'l') l++;
      else if (i == 'o') o++;
      else if (i == 'n') n++;
    }
    return Math.min(b, a, l >> 1, o >> 1, n);
  }
}
```

## Word Pattern

https://neetcode.io/problems/word-pattern/question

```js
class Solution {
  /**
   * @param {string} pattern
   * @param {string} s
   * @return {boolean}
   */
  wordPattern(pattern, s) {
    const a = [...pattern];
    const b = s.split(' ');
    if (a.length != b.length) return false;
    let c1 = Object.create(null);
    let c2 = Object.create(null);
    for (let i = 0; i < a.length; i++) {
      if (c1[a[i]] && c1[a[i]] != b[i]) return false;
      if (c2[b[i]] && c2[b[i]] != a[i]) return false;
      c1[a[i]] = b[i];
      c2[b[i]] = a[i];
    }
    return true;
  }
}
```

```js
class Solution {
  /**
   * @param {string} pattern
   * @param {string} s
   * @return {boolean}
   */
  wordPattern(pattern, s) {
    const a = [...pattern];
    const b = s.split(' ');
    if (a.length != b.length) return false;
    if (new Set(a).size != new Set(b).size) return false;
    let c = {};
    for (let i = 0; i < a.length; i++) {
      if (c[a[i]] && c[a[i]] != b[i]) return false;
      c[a[i]] = b[i];
    }
    return true;
  }
}
```

## Design Hashset

https://neetcode.io/problems/design-hashset/question

```js
class MyHashSet {
  constructor() {
    this.hash = {};
  }

  /**
   * @param {number} key
   * @return {void}
   */
  add(key) {
    this.hash[key] = true;
  }

  /**
   * @param {number} key
   * @return {void}
   */
  remove(key) {
    delete this.hash[key];
  }

  /**
   * @param {number} key
   * @return {boolean}
   */
  contains(key) {
    return !(key in this.hash);
  }
}

/**
 * Your MyHashSet object will be instantiated and called as such:
 * var obj = new MyHashSet()
 * obj.add(key)
 * obj.remove(key)
 * var param_3 = obj.contains(key)
 */
```

## Design HashMap

https://neetcode.io/problems/design-hashmap/question

```js
class MyHashMap {
  constructor() {
    this.hash = {};
  }

  /**
   * @param {number} key
   * @param {number} value
   * @return {void}
   */
  put(key, value) {
    this.hash[key] = value;
  }

  /**
   * @param {number} key
   * @return {number}
   */
  get(key) {
    return key in this.hash ? this.hash[key] : -1;
  }

  /**
   * @param {number} key
   * @return {void}
   */
  remove(key) {
    delete this.hash[key];
  }
}

/**
 * Your MyHashMap object will be instantiated and called as such:
 * var obj = new MyHashMap()
 * obj.put(key,value)
 * var param_2 = obj.get(key)
 * obj.remove(key)
 */
```

## Height Checker

https://neetcode.io/problems/height-checker/question

```js
class Solution {
  /**
   * @param {number[]} heights
   * @return {number}
   */
  heightChecker(nums) {
    const nums0 = nums.slice();
    const nums1 = nums.sort((x1, x2) => x1 - x2);
    let a = 0;
    for (let i = 0; i < nums.length; i++) a = nums0[i] != nums1[i] ? a + 1 : a;
    return a;
  }
}
```

## Find Lucky Integer in an Array

https://neetcode.io/problems/find-lucky-integer-in-an-array/question

```js
class Solution {
  /**
   * @param {number[]} arr
   * @return {number}
   */
  findLucky(arr) {
    let a = {},
      b = -1;
    for (let i of arr) a[i] = (a[i] ?? 0) + 1;
    for (let i in a) {
      if (+i == a[i]) b = a[i] > b ? a[i] : b;
    }
    return b;
  }
}
```

## Special Array I

https://neetcode.io/problems/special-array-i/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  isArraySpecial(nums) {
    for (let i = 1; i < nums.length; i++) {
      if (nums[i] % 2 == nums[i - 1] % 2) return false;
    }
    return true;
  }
}
```

## Check if Array Is Sorted and Rotated

https://neetcode.io/problems/check-if-array-is-sorted-and-rotated/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  check(nums) {
    let a = true;
    for (let i = 1; i < nums.length; i++) {
      if (nums[i] < nums[i - 1]) {
        if (!a) return false;
        a = false;
      }
    }
    return a || nums[0] >= nums.at(-1);
  }
}
```

## Monotonic Array

https://neetcode.io/problems/monotonic-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  isMonotonic(nums) {
    let a1 = true,
      a2 = true,
      i = 1;
    while ((a1 || a2) && i < nums.length) {
      a1 = a1 && nums[i] >= nums[i - 1];
      a2 = a2 && nums[i] <= nums[i - 1];
      i++;
    }
    return a1 || a2;
  }
}
```

## Divide Array Into Equal Pairs

https://neetcode.io/problems/divide-array-into-equal-pairs/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  divideArray(nums) {
    let a = {};
    for (let i of nums) a[i] = (a[i] ?? 0) + 1;
    return Object.values(a).reduce((a, x) => a && x % 2 == 0, true);
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {boolean}
   */
  divideArray(nums) {
    let a = {};
    for (let i of nums) a[i] = (a[i] ?? 0) + 1;
    return Object.values(a).every((x) => !(x & 1));
  }
}
```

## Number of Good Pairs

https://neetcode.io/problems/number-of-good-pairs/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  numIdenticalPairs(nums) {
    let a = 0;
    for (let i = 0; i < nums.length; i++) {
      for (let j = i + 1; j < nums.length; j++) {
        a = nums[i] == nums[j] ? a + 1 : a;
      }
    }
    return a;
  }
}
```

## Pascal's Triangle II

https://neetcode.io/problems/pascals-triangle-ii/question

```js
class Solution {
  /**
   * @param {number} rowIndex
   * @return {number[]}
   */
  getRow(rowIndex) {
    const fact = (n) => {
      if (n < 2) return 1;
      return n * fact(n - 1);
    };

    let a = [];
    for (let i = 0; i <= rowIndex; i++) a.push((fact(rowIndex) / fact(i) / fact(rowIndex - i)) | 0);
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number} rowIndex
   * @return {number[]}
   */
  getRow(rowIndex) {
    //C(n, k) = C(n, k-1) * (n - k + 1) / k
    let a = [1];
    for (let i = 1; i <= rowIndex; i++) {
      a[i] = (a[i - 1] * (rowIndex - i + 1)) / i;
    }
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number} rowIndex
   * @return {number[]}
   */
  getRow(rowIndex) {
    let a = Array(rowIndex + 1).fill(1);
    for (let i = 1; i < rowIndex; i++) {
      for (let j = i; j > 0; j--) {
        a[j] += a[j - 1];
      }
    }
    return a;
  }
}
```

## Find Words That Can Be Formed by Characters

https://neetcode.io/problems/find-words-that-can-be-formed-by-characters/question

```js
class Solution {
  /**
   * @param {string[]} words
   * @param {string} chars
   * @return {number}
   */
  countCharacters(words, chars) {
    let a0 = {},
      a;
    let b = 0,
      c;
    for (let i of chars) a0[i] = (a0[i] ?? 0) + 1;
    for (let s of words) {
      a = { ...a0 };
      c = true;
      for (let i of s) {
        if (!a[i]) {
          c = false;
          break;
        }
        a[i]--;
      }
      if (c) b += s.length;
    }
    return b;
  }
}
```

## Count the Number of Consistent Strings

https://neetcode.io/problems/count-the-number-of-consistent-strings/question

```js
class Solution {
  /**
   * @param {string} allowed
   * @param {string[]} words
   * @return {number}
   */
  countConsistentStrings(allowed, words) {
    let a = 0;
    let b = new Set(allowed);
    for (let i of words) {
      if ([...i].every((x) => b.has(x))) a++;
    }
    return a;
  }
}
```

## Ransom Note

https://neetcode.io/problems/ransom-note/question

```js
class Solution {
  /**
   * @param {string} ransomNote
   * @param {string} magazine
   * @return {boolean}
   */
  canConstruct(ransomNote, magazine) {
    let a = {};
    for (let i of magazine) a[i] = (a[i] ?? 0) + 1;
    for (let i of ransomNote) {
      if (!a[i]) return false;
      a[i]--;
    }
    return true;
  }
}
```

## Largest 3-Same-Digit Number in String

https://neetcode.io/problems/largest-3-same-digit-number-in-string/question

```js
class Solution {
  /**
   * @param {string} num
   * @return {string}
   */
  largestGoodInteger(num) {
    let a = '';
    for (let i = 2; i < num.length; i++) {
      if (num[i - 2] == num[i] && num[i - 1] == num[i]) {
        a = num[i] > a ? num[i] : a;
      }
    }
    return a + a + a;
  }
}
```

## Destination City

https://leetcode.com/problems/destination-city/description/

```js
/**
 * @param {string[][]} paths
 * @return {string}
 */
const destCity = (paths) => {
  let a = new Set(),
    b = new Set();
  for (let i of paths) {
    a.add(i[0]);
    b.add(i[1]);
  }
  for (let i of b) if (!a.has(i)) return i;
};
```

## Maximum Product Difference Between Two Pairs

https://neetcode.io/problems/maximum-product-difference-between-two-pairs/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  maxProductDifference(nums) {
    nums.sort((x1, x2) => x2 - x1);
    return nums[0] * nums[1] - nums.at(-1) * nums.at(-2);
  }
}
```

## Circular Sentence

https://leetcode.com/problems/circular-sentence/description/

```js
/**
 * @param {string} sentence
 * @return {boolean}
 */
const isCircularSentence = (sentence) => {
  let a = sentence.split(' ');
  if (a[0][0] != a.at(-1).at(-1)) return false;
  for (let i = 1; i < a.length; i++) {
    if (a[i - 1].at(-1) != a[i][0]) return false;
  }
  return true;
};
```

## Maximum Score After Splitting a String

https://neetcode.io/problems/maximum-score-after-splitting-a-string/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  maxScore(s) {
    let a = 0,
      b = 0,
      c = 0;
    for (let i of s) a = i == '1' ? a + 1 : a;
    for (let i of s.slice(0, -1)) {
      if (i == '0') b++;
      else a--;
      c = a + b > c ? a + b : c;
    }
    return c;
  }
}
```

## Path Crossing

https://neetcode.io/problems/path-crossing/question

```js
class Solution {
  /**
   * @param {string} path
   * @return {boolean}
   */
  isPathCrossing(path) {
    let x = 0,
      y = 0;
    let a = new Set();
    a.add(x + ',' + y);
    for (let i of Array.from(path)) {
      x = i == 'W' ? x - 1 : i == 'E' ? x + 1 : x;
      y = i == 'N' ? y - 1 : i == 'S' ? y + 1 : y;
      a.add(x + ',' + y);
    }
    return !(path.length + 1 == a.size);
  }
}
```

## Minimum Changes To Make Alternating Binary String

https://neetcode.io/problems/minimum-changes-to-make-alternating-binary-string/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  minOperations(s) {
    let a = 0,
      b = 0,
      c = 1,
      d = 0;
    for (let i of Array.from(s)) {
      a = i == c ? a + 1 : a;
      b = i == d ? b + 1 : b;
      [c, d] = [d, c];
    }
    return Math.min(a, b);
  }
}
```

## Redistribute Characters to Make All Strings Equal

https://neetcode.io/problems/redistribute-characters-to-make-all-strings-equal/question

```js
class Solution {
  /**
   * @param {string[]} words
   * @return {boolean}
   */
  makeEqual(words) {
    let a = {};
    for (let i of words.join('')) a[i] = (a[i] ?? 0) + 1;
    return Object.values(a).every((x) => x % words.length == 0);
  }
}
```

## Longest Palindrome

https://leetcode.com/problems/longest-palindrome/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const longestPalindrome = (s) => {
  let a = {};
  for (let i of s) a[i] = (a[i] ?? 0) + 1;
  let b = 0;
  let c = false;
  for (let i of Object.values(a)) {
    if (i % 2 == 0) {
      b += i;
    } else {
      b += i - 1;
      c = true;
    }
  }
  return c ? b + 1 : b;
};
```

```js
/**
 * @param {string} s
 * @return {number}
 */
const longestPalindrome = (s) => {
  let a = new Set();
  let b = 0;
  for (let i of s) {
    if (a.has(i)) {
      a.delete(i);
      b += 2;
    } else {
      a.add(i);
    }
  }
  return a.size > 0 ? b + 1 : b;
};
```

## Largest Substring Between Two Equal Characters

https://leetcode.com/problems/largest-substring-between-two-equal-characters/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const maxLengthBetweenEqualCharacters = (s) => {
  let a = {};
  let b = -1;
  for (let i = 0; i < s.length; i++) {
    a[s[i]] ??= i;
    b = Math.max(b, i - a[s[i]] - 1);
  }
  return b;
};
```

## Set Mismatch

https://leetcode.com/problems/set-mismatch/description/

```js
/**
 * @param {number[]} nums
 * @return {number[]}
 */
const findErrorNums = (nums) => {
  const n = nums.length;
  const a1 = nums.reduce((a, x) => a + x, 0);
  const b1 = (n * (n + 1)) / 2;
  const a2 = nums.reduce((a, x) => a + x ** 2, 0);
  const b2 = (n * (n + 1) * (2 * n + 1)) / 6;
  const c1 = a1 - b1;
  const c2 = (a2 - b2) / c1;
  return [(c1 + c2) / 2, (c2 - c1) / 2];
};
```

## First Unique Character in a String

https://neetcode.io/problems/first-unique-character-in-a-string/question?list=allNC

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  firstUniqChar(s) {
    let a = {};
    for (let i = 0; i < s.length; i++) a[s[i]] = s[i] in a ? Infinity : i;
    let b = Math.min(...Object.values(a));
    return b === Infinity ? -1 : b;
  }
}
```

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  firstUniqChar(s) {
    let a = {};
    for (let i of s) a[i] = (a[i] ?? 0) + 1;
    for (let i = 0; i < s.length; i++) if (a[s[i]] == 1) return i;
    return -1;
  }
}
```

## Intersection of Two Arrays

https://neetcode.io/problems/intersection-of-two-arrays/question

```js
class Solution {
  /**
   * @param {number[]} nums1
   * @param {number[]} nums2
   * @return {number[]}
   */
  intersection(nums1, nums2) {
    let a = [];
    let b = new Set(nums1);
    let c = new Set(nums2);
    for (let i of b) {
      if (c.has(i)) a.push(i);
    }
    return a;
  }
}
```

## Find Common Characters

https://leetcode.com/problems/find-common-characters/description/

```js
/**
 * @param {string[]} words
 * @return {string[]}
 */
const commonChars = (words) => {
  let a = [];
  let b = Infinity,
    c = '';
  for (let s of words) [b, c] = s.length < b ? [s.length, s] : [b, c];
  for (let i of c) {
    if (words.every((x) => x.includes(i))) {
      words = words.map((x) => x.replace(i, ''));
      console.log(i, words);
      a.push(i);
    }
  }
  return a;
};
```

## Number of Students Unable to Eat Lunch

https://neetcode.io/problems/number-of-students-unable-to-eat-lunch/question

```js
class Solution {
  /**
   * @param {number[]} students
   * @param {number[]} sandwiches
   * @return {number}
   */
  countStudents(students, sandwiches) {
    let a = true;
    while (a && sandwiches.length) {
      a = false;
      for (let i = 0; i < students.length; i++) {
        if (students[i] == sandwiches[0]) {
          sandwiches.shift();
          students[i] = -1;
          a = true;
        }
      }
    }
    return sandwiches.length;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} students
   * @param {number[]} sandwiches
   * @return {number}
   */
  countStudents(students, sandwiches) {
    let a = 0;
    while (students.length && a < students.length) {
      if (students[0] == sandwiches[0]) {
        students.shift();
        sandwiches.shift();
        a = 0;
      } else {
        students.push(students.shift());
        a++;
      }
    }
    return students.length;
  }
}
```

## Time Needed to Buy Tickets

https://leetcode.com/problems/time-needed-to-buy-tickets/description/

```js
/**
 * @param {number[]} tickets
 * @param {number} k
 * @return {number}
 */
const timeRequiredToBuy = (tickets, k) => {
  let a = 0;
  for (let i = 0; i < tickets.length; i++) {
    if (i <= k) a += Math.min(tickets[i], tickets[k]);
    else a += Math.min(tickets[i], tickets[k] - 1);
  }
  return a;
};
```

## Special Array With X Elements Greater Than or Equal X

https://leetcode.com/problems/special-array-with-x-elements-greater-than-or-equal-x/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const specialArray = (nums) => {
  const n = nums.length;
  nums.sort((x1, x2) => x2 - x1);
  if (nums.at(-1) >= n) return n;
  for (let i = 1; i < nums.length; i++) {
    if (nums[i - 1] >= i && nums[i] < i) return i;
  }
  return -1;
};
```

## Relative Sort Array

https://leetcode.com/problems/relative-sort-array/description/

```js
/**
 * @param {number[]} arr1
 * @param {number[]} arr2
 * @return {number[]}
 */
const relativeSortArray = (arr1, arr2) => {
  let a = {};
  for (let i of arr1) a[i] = (a[i] ?? 0) + 1;
  let b = [];
  for (let i of arr2) {
    while (a[i] > 0) {
      b.push(i);
      a[i]--;
    }
  }
  let c = [];
  for (let i in a) {
    while (a[i] > 0) {
      c.push(+i);
      a[i]--;
    }
  }
  return [...b, ...c.sort((x1, x2) => x1 - x2)];
};
```

```js
/**
 * @param {number[]} arr1
 * @param {number[]} arr2
 * @return {number[]}
 */
const relativeSortArray = (arr1, arr2) => {
  const a = new Map(arr2.map((v, i) => [v, i]));
  return arr1.sort((x1, x2) => {
    if (a.has(x1) && a.has(x2)) return a.get(x1) - a.get(x2);
    if (a.has(x1)) return -1;
    if (a.has(x2)) return 1;
    return x1 - x2;
  });
};
```

## Sort the People

https://leetcode.com/problems/sort-the-people/description/

```js
/**
 * @param {string[]} names
 * @param {number[]} heights
 * @return {string[]}
 */
const sortPeople = (names, heights) => {
  let a = [];
  for (let i = 0; i < names.length; i++) a.push([names[i], heights[i]]);
  a.sort((x1, x2) => x2[1] - x1[1]);
  let b = [];
  for (let [i, _] of a) b.push(i);
  return b;
};
```

## Sort Array by Increasing Frequency

https://neetcode.io/problems/sort-array-by-increasing-frequency/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  frequencySort(nums) {
    const a = {};
    for (let i of nums) a[i] = (a[i] ?? 0) + 1;
    return nums.sort((x1, x2) => {
      if (a[x1] != a[x2]) return a[x1] - a[x2];
      return x2 - x1;
    });
  }
}
```

## Find The Index of The First Occurrence in a String

https://neetcode.io/problems/find-the-index-of-the-first-occurrence-in-a-string/question

```js
class Solution {
  /**
   * @param {string} haystack
   * @param {string} needle
   * @return {number}
   */
  strStr(haystack, needle) {
    return haystack.indexOf(needle);
  }
}
```

## Sign of the Product of an Array

https://leetcode.com/problems/sign-of-the-product-of-an-array/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const arraySign = (nums) => {
  return nums.reduce((a, x) => Math.sign(a * x), 1);
};
```

## Find the Difference of Two Arrays

https://neetcode.io/problems/find-the-difference-of-two-arrays/question

```js
class Solution {
  /**
   * @param {number[]} nums1
   * @param {number[]} nums2
   * @return {number[][]}
   */
  findDifference(nums1, nums2) {
    let a = new Set(nums1),
      b = new Set(nums2);
    for (let i of nums2) if (a.has(i)) a.delete(i);
    for (let i of nums1) if (b.has(i)) b.delete(i);
    return [[...a], [...b]];
  }
}
```

## Uncommon Words from Two Sentences

https://leetcode.com/problems/uncommon-words-from-two-sentences/description/

```js
/**
 * @param {string} s1
 * @param {string} s2
 * @return {string[]}
 */
const uncommonFromSentences = (s1, s2) => {
  let a = {};
  for (let i of [...s1.split(' '), ...s2.split(' ')]) a[i] = (a[i] ?? 0) + 1;
  let b = [];
  for (let i in a) if (a[i] == 1) b.push(i);
  return b;
};
```

## Design Parking System

https://leetcode.com/problems/design-parking-system/description/

```js
/**
 * @param {number} big
 * @param {number} medium
 * @param {number} small
 */
var ParkingSystem = function (big, medium, small) {
  this.slots = [big, medium, small];
};

/**
 * @param {number} carType
 * @return {boolean}
 */
ParkingSystem.prototype.addCar = function (carType) {
  if (this.slots[carType - 1] > 0) {
    this.slots[carType - 1]--;
    return true;
  }
  return false;
};
```

---

---

---

# Stack

## Crawler Log Folder

https://neetcode.io/problems/crawler-log-folder/question?

```js
class Solution {
  /**
   * @param {string[]} logs
   * @return {number}
   */
  minOperations(logs) {
    let a = 0;
    for (let i of logs) {
      if (i == '../') a = a > 0 ? a - 1 : a;
      else if (i != './') a++;
    }
    return a;
  }
}
```

## Baseball Game

https://neetcode.io/problems/baseball-game/question

```js
class Solution {
  /**
   * @param {string[]} operations
   * @return {number}
   */
  calPoints(operations) {
    let a = [];
    for (let i = 0; i < operations.length; i++) {
      const b = operations[i];
      const c = a.length;
      if (b == '+') {
        a.push(a[c - 1] * 1 + a[c - 2] * 1);
      } else if (b == 'D') {
        a.push(a[c - 1] * 2);
      } else if (b == 'C') {
        a.pop();
      } else {
        a.push(+b);
      }
    }
    return a.reduce((a, x) => a + x, 0);
  }
}
```

## Valid Parentheses

https://neetcode.io/problems/validate-parentheses/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {boolean}
   */
  isValid(s) {
    let n = s.length;
    while (true) {
      const s1 = s.replace('()', '').replace('[]', '').replace('{}', '');
      const n1 = s1.length;
      if (n1 == 0) return true;
      else if (n == n1) return false;
      s = s1;
      n = n1;
    }
  }
}
```

```js
class Solution {
  /**
   * @param {string} s
   * @return {boolean}
   */
  isValid(s) {
    let a = [];
    a.push(s[0]);
    for (let i = 1; i < s.length; i++) {
      const b = s[i],
        c = a[a.length - 1];
      if (b == ')') {
        if (c == '(') a.pop();
        else return false;
      } else if (b == ']') {
        if (c == '[') a.pop();
        else return false;
      } else if (b == '}') {
        if (c == '{') a.pop();
        else return false;
      } else a.push(b);
    }
    return a.length == 0;
  }
}
```

## Implement Stack Using Queues

https://neetcode.io/problems/implement-stack-using-queues/question

```js
class MyStack {
  constructor() {
    this.a = [];
  }

  /**
   * @param {number} x
   * @return {void}
   */
  push(x) {
    this.a.push(x);
  }

  /**
   * @return {number}
   */
  pop() {
    return this.a.pop();
  }

  /**
   * @return {number}
   */
  top() {
    return this.a[this.a.length - 1];
  }

  /**
   * @return {boolean}
   */
  empty() {
    return this.a.length == 0;
  }
}

/**
 * Your MyStack object will be instantiated and called as such:
 * var obj = new MyStack()
 * obj.push(x)
 * var param_2 = obj.pop()
 * var param_3 = obj.top()
 * var param_4 = obj.empty()
 */
```

## Implement Queue using Stacks

https://neetcode.io/problems/implement-queue-using-stacks/question

```js
class MyQueue {
  constructor() {
    this.a = [];
  }

  /**
   * @param {number} x
   * @return {void}
   */
  push(x) {
    this.a.push(x);
  }

  /**
   * @return {number}
   */
  pop() {
    return this.a.shift();
  }

  /**
   * @return {number}
   */
  peek() {
    return this.a[0];
  }

  /**
   * @return {boolean}
   */
  empty() {
    return this.a.length == 0;
  }
}

/**
 * Your MyQueue object will be instantiated and called as such:
 * var obj = new MyQueue()
 * obj.push(x)
 * var param_2 = obj.pop()
 * var param_3 = obj.peek()
 * var param_4 = obj.empty()
 */
```

## Final Prices With a Special Discount in a Shop

https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/description/

```js
/**
 * @param {number[]} prices
 * @return {number[]}
 */
const finalPrices = (prices) => {
  const a = [];
  for (let i = 0; i < prices.length; i++) {
    while (a.length && prices[a.at(-1)] >= prices[i]) {
      const j = a.pop();
      prices[j] -= prices[i];
    }
    a.push(i);
  }
  return prices;
};
```

## Make the String Great

https://leetcode.com/problems/make-the-string-great/description/

```js
/**
 * @param {string} s
 * @return {string}
 */
const makeGood = (s) => {
  let a = [];
  for (let i of s) {
    if (a.length && Math.abs(a.at(-1).charCodeAt(0) - i.charCodeAt(0)) == 32) a.pop();
    else a.push(i);
  }
  return a.join('');
};
```

## Minimum String Length After Removing Substrings

https://leetcode.com/problems/minimum-string-length-after-removing-substrings/editorial/

```js
/**
 * @param {string} s
 * @return {number}
 */
const minLength = (s) => {
  let a = [];
  for (let i of s) {
    if ((a.length && a.at(-1) + i == 'AB') || a.at(-1) + i == 'CD') a.pop();
    else a.push(i);
  }
  return a.length;
};
```

## Clear Digits

https://leetcode.com/problems/clear-digits/description/

```js
/**
 * @param {string} s
 * @return {string}
 */
const clearDigits = (s) => {
  a = [];
  for (let i of s) {
    if (/[a-z]/.test(a.at(-1)) && /[0-9]/.test(i)) a.pop();
    else a.push(i);
  }
  return a.join('');
};
```

---

---

---

# Two Pointers

## Reverse String

https://neetcode.io/problems/reverse-string/question

```js
class Solution {
  /**
   * @param {character[]} s
   * @return {void} Do not return anything, modify s in-place instead.
   */
  reverseString(s) {
    return s.reverse();
  }
}
```

## Valid Palindrome

https://neetcode.io/problems/is-palindrome/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {boolean}
   */
  isPalindrome(s) {
    const re = /[^a-z0-9]/g;
    const ss = s.toLowerCase().replace(re, '');
    let l = 0,
      r = ss.length - 1;
    while (l < r) if (ss[l++] != ss[r--]) return false;
    return true;
  }
}
```

## Valid Palindrome II

https://neetcode.io/problems/valid-palindrome-ii/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {boolean}
   */
  isPalindrome(s) {
    const ss = s;
    //const re=/[^a-z0-9]/g
    //const ss=s.toLowerCase().replace(re,'');
    let l = 0,
      r = ss.length - 1;
    while (l < r) if (ss[l++] != ss[r--]) return false;
    return true;
  }

  /**
   * @param {string} s
   * @return {boolean}
   */
  validPalindrome(s) {
    if (s.length < 3) return true;
    let l = 0,
      r = s.length - 1;
    while (l < r) {
      if (s[l] != s[r]) {
        return this.isPalindrome(s.slice(l, r)) || this.isPalindrome(s.slice(l + 1, r + 1));
      }
      l++;
      r--;
    }
    return true;
  }
}
```

## Valid Word Abbreviation

https://neetcode.io/problems/valid-word-abbreviation/question

```js
class Solution {
  /**
   * @param {string} word
   * @param {string} abbr
   * @return {boolean}
   */
  validWordAbbreviation(word, abbr) {
    let i1 = 0,
      i2 = 0;
    while (i1 < word.length && i2 < abbr.length) {
      if (isNaN(abbr[i2])) {
        if (word[i1] != abbr[i2]) return false;
        (i1++, i2++);
      } else {
        if (abbr[i2] == '0') return false;
        let a = 0;
        while (i2 < abbr.length && !isNaN(abbr[i2])) {
          a = a * 10 + (abbr[i2] - '0');
          i2++;
        }
        i1 += a;
      }
    }
    return i1 == word.length && i2 == abbr.length;
  }
}
```

## Merge Strings Alternately

https://neetcode.io/problems/merge-strings-alternately/question

```js
class Solution {
  /**
   * @param {string} word1
   * @param {string} word2
   * @return {string}
   */
  mergeAlternately(word1, word2) {
    const n = Math.min(word1.length, word2.length);
    let c = '';
    for (let i = 0; i < n; i++) c += word1[i] + word2[i];
    c += word1.slice(n) + word2.slice(n);
    return c;
  }
}
```

## Merge Sorted Array

https://neetcode.io/problems/merge-sorted-array/question

```js
class Solution {
  /**
   * @param {number[]} nums1
   * @param {number} m
   * @param {number[]} nums2
   * @param {number} n
   * @return {void} Do not return anything, modify nums1 in-place instead.
   */
  merge(nums1, m, nums2, n) {
    for (let i = m; i < m + n; i++) nums1[i] = nums2[i - m];
    nums1.sort((x1, x2) => x1 - x2);
  }
}
```

## Merge Two 2D Arrays by Summing Values

https://leetcode.com/problems/merge-two-2d-arrays-by-summing-values/description/

```js
/**
 * @param {number[][]} nums1
 * @param {number[][]} nums2
 * @return {number[][]}
 */
const mergeArrays = (nums1, nums2) => {
  let a = {};
  for (let [k, v] of [...nums1, ...nums2]) a[k] = (a[k] ?? 0) + v;
  return Object.entries(a)
    .map((x) => [+x[0], x[1]])
    .sort((x1, x2) => x1[0] - x2[0]);
};
```

## Move Zeroes

https://neetcode.io/problems/move-zeroes/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {void} Do not return anything, modify nums in-place instead.
   */
  moveZeroes(nums) {
    let i1 = 0;
    for (let i2 = 0; i2 < nums.length; i2++) {
      if (nums[i2] != 0) {
        [nums[i1], nums[i2]] = [nums[i2], nums[i1]];
        i1++;
      }
    }
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {void} Do not return anything, modify nums in-place instead.
   */
  moveZeroes(nums) {
    let i1 = 0;
    for (let i of nums) if (i != 0) nums[i1++] = i;
    while (i1 < nums.length) nums[i1++] = 0;
    return nums;
  }
}
```

## Remove Duplicates From Sorted Array

https://neetcode.io/problems/remove-duplicates-from-sorted-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  removeDuplicates(nums) {
    let k = 0;
    for (let i = 1; i < nums.length; i++) {
      if (nums[i] != nums[k]) k++;
      nums[k] = nums[i];
    }
    return k + 1;
  }
}
```

## Squares of a Sorted Array

https://neetcode.io/problems/squares-of-a-sorted-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  sortedSquares(nums) {
    return nums.map((x) => x ** 2).sort((x1, x2) => x1 - x2);
  }
}
```

## Assign Cookies

https://neetcode.io/problems/assign-cookies/question

```js
class Solution {
  /**
   * @param {number[]} g
   * @param {number[]} s
   * @return {number}
   */
  findContentChildren(g, s) {
    g.sort((x1, x2) => x1 - x2);
    s.sort((x1, x2) => x1 - x2);
    const n = s.length;
    while (g.length) if (g.pop() <= s.at(-1)) s.pop();
    return n - s.length;
  }
}
```

## Find First Palindromic String in the Array

https://leetcode.com/problems/find-first-palindromic-string-in-the-array/description/

```js
/**
 * @param {string[]} words
 * @return {string}
 */
const firstPalindrome = (words) => {
  for (let s of words) {
    let i1 = 0,
      i2 = s.length - 1;
    while (s[i1++] == s[i2--]) {
      if (i1 >= i2) return s;
    }
  }
  return '';
};
```

## Sort Array by Parity

https://neetcode.io/problems/sort-array-by-parity/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  sortArrayByParity(nums) {
    let a = [],
      b = [];
    for (let i of nums) {
      if (i % 2 == 0) a.push(i);
      else b.push(i);
    }
    return [...a, ...b];
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  sortArrayByParity(nums) {
    let i1 = 0;
    for (let i2 = 0; i2 < nums.length; i2++) {
      if (nums[i2] % 2 == 0) {
        [nums[i1], nums[i2]] = [nums[i2], nums[i1]];
        i1++;
      }
    }
    return nums;
  }
}
```

## Reverse Words in a String III

https://leetcode.com/problems/reverse-words-in-a-string-iii/description/

```js
/**
 * @param {string} s
 * @return {string}
 */
const reverseWords = (s) => {
  return s
    .split(' ')
    .map((x) => x.split('').reverse().join(''))
    .join(' ');
};
```

## Backspace String Compare

https://leetcode.com/problems/backspace-string-compare/description/

```js
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
const backspaceCompare = (s, t) => {
  let a = [],
    b = [];
  for (let i of s) {
    if (i == '##') a.pop();
    else a.push(i);
  }
  for (let i of t) {
    if (i == '##') b.pop();
    else b.push(i);
  }
  return a.join('') == b.join('');
};
```

```js
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
const fn = (str) => {
  const a = [];
  for (let i of str) i == '##' ? a.pop() : a.push(i);
  return a.join('');
};

const backspaceCompare = (s, t) => fn(s) == fn(t);
```

## Check If Two String Arrays are Equivalent

https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent/description/

```js
/**
 * @param {string[]} word1
 * @param {string[]} word2
 * @return {boolean}
 */
const arrayStringsAreEqual = (word1, word2) => {
  return word1.join('') == word2.join('');
};
```

## Apply Operations to an Array

https://leetcode.com/problems/apply-operations-to-an-array/description/

```js
/**
 * @param {number[]} nums
 * @return {number[]}
 */
const applyOperations = (nums) => {
  for (let i = 1; i < nums.length; i++) {
    if (nums[i - 1] == nums[i]) {
      nums[i - 1] *= 2;
      nums[i] = 0;
    }
  }
  let i1 = 0;
  for (let i of nums) if (i != 0) nums[i1++] = i;
  while (i1 < nums.length) nums[i1++] = 0;
  return nums;
};
```

---

---

---

# Sliding Window

## Contains Duplicate II

https://neetcode.io/problems/contains-duplicate-ii/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {boolean}
   */
  containsNearbyDuplicate(nums, k) {
    const s = new Set();
    for (let i = 0; i < nums.length; i++) {
      if (s.has(nums[i])) return true;
      s.add(nums[i]);
      if (s.size > k) s.delete(nums[i - k]);
    }
    return false;
  }
}
```

## Best Time to Buy and Sell Stock

https://neetcode.io/problems/buy-and-sell-crypto/question

```js
class Solution {
  /**
   * @param {number[]} prices
   * @return {number}
   */
  maxProfit(prices) {
    let a = 0,
      b = prices[0];
    for (let i = 1; i < prices.length; i++) {
      a = Math.max(prices[i] - b, a);
      b = Math.min(prices[i], b);
    }
    return a;
  }
}
```

## Minimum Recolors to Get K Consecutive Black Blocks

https://neetcode.io/problems/minimum-recolors-to-get-k-consecutive-black-blocks/question

```js
class Solution {
  /**
   * @param {string} blocks
   * @param {number} k
   * @return {number}
   */
  minimumRecolors(blocks, k) {
    let a = blocks.slice(0, k).replaceAll('B', '').length;
    let a0 = a;
    for (let i = k; i < blocks.length; i++) {
      a = a - (blocks[i - k] == 'W' ? 1 : 0) + (blocks[i] == 'W' ? 1 : 0);
      a0 = a < a0 ? a : a0;
    }
    return a0;
  }
}
```

## Minimum Difference Between Highest And Lowest of K Scores

https://neetcode.io/problems/minimum-difference-between-highest-and-lowest-of-k-scores/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  minimumDifference(nums, k) {
    nums.sort((x1, x2) => x1 - x2);
    let a = Infinity;
    k--;
    for (let i = k; i < nums.length; i++) {
      a = nums[i] - nums[i - k] < a ? nums[i] - nums[i - k] : a;
    }
    return a;
  }
}
```

## Defuse the Bomb

https://leetcode.com/problems/defuse-the-bomb/description/

```js
/**
 * @param {number[]} code
 * @param {number} k
 * @return {number[]}
 */
const mod = (a, m) => ((a % m) + m) % m;

const decrypt = (code, k) => {
  const n = code.length;
  let a = [];
  for (let i1 = 0; i1 < code.length; i1++) {
    let b = 0;
    if (k > 0) {
      for (let i2 = i1 + 1; i2 <= i1 + k; i2++) b += code[mod(i2, n)];
    } else {
      for (let i2 = i1 - 1; i2 >= i1 + k; i2--) b += code[mod(i2, n)];
    }
    a.push(b);
  }
  return a;
};
```

```js
/**
 * @param {number[]} code
 * @param {number} k
 * @return {number[]}
 */
const decrypt = (code, k) => {
  const n = code.length;
  let a = Array(n).fill(0);
  if (k == 0) return a;
  let b = 0;
  let l, r;
  [l, r] = k > 0 ? [1, k] : [k, -1];
  for (let i = l; i <= r; i++) b += code[(i + n) % n];
  for (let i = 0; i < n; i++) {
    a[i] = b;
    b -= code[(l + i + n) % n];
    b += code[(r + i + 1 + n) % n];
  }
  return a;
};
```

---

---

---

# Binary Search

## Binary Search

https://neetcode.io/problems/binary-search/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number}
   */
  search(nums, target) {
    let l = 0,
      r = nums.length - 1,
      m;
    while (l <= r) {
      m = Math.floor((l + r) / 2);
      //console.log([l,r,m]);
      if (nums[m] == target) return m;
      [l, r] = nums[m] < target ? [m + 1, r] : [l, m - 1];
    }
    return -1;
  }
}
```

## Search Insert Position

https://neetcode.io/problems/search-insert-position/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number}
   */
  searchInsert(nums, target) {
    let l = 0,
      r = nums.length - 1,
      m;
    while (l <= r) {
      m = Math.floor((l + r) / 2);
      //console.log([l,r,m]);
      if (nums[m] == target) return m;
      [l, r] = nums[m] < target ? [m + 1, r] : [l, m - 1];
    }
    return nums[m] < target ? m + 1 : m;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number}
   */
  searchInsert(nums, target) {
    let l = 0,
      r = nums.length - 1;
    while (l <= r) {
      const m = Math.floor((l + r) / 2);
      if (nums[m] === target) return m;
      if (nums[m] < target) {
        l = m + 1;
      } else {
        r = m - 1;
      }
    }
    return l;
  }
}
```

## Guess Number Higher Or Lower

https://neetcode.io/problems/guess-number-higher-or-lower/question

```js
/**
 * Forward declaration of guess API.
 * @param {number} num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * function guess(num) {}
 */

class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  guessNumber(n) {
    let l = 1,
      r = n,
      m;
    while (l <= r) {
      m = Math.floor((l + r) / 2);
      if (guess(m) == 0) return m;
      [l, r] = guess(m) > 0 ? [m + 1, r] : [l, m - 1];
    }
  }
}
/**
 * Forward declaration of guess API.
 * @param {number} num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * function guess(num) {}
 */

class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  guessNumber(n) {
    let l = 1,
      r = n,
      m;
    while (l <= r) {
      m = Math.floor((l + r) / 2);
      if (guess(m) == 0) return m;
      [l, r] = guess(m) > 0 ? [m + 1, r] : [l, m - 1];
    }
  }
}
```

## Arranging Coins

https://neetcode.io/problems/arranging-coins/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  arrangeCoins(n) {
    let a = 1;
    while ((a * (a + 1)) / 2 <= n) a++;
    return a - 1;
  }
}
```

## Valid Perfect Square

https://neetcode.io/problems/valid-perfect-square/question

```js
class Solution {
  /**
   * @param {number} num
   * @return {boolean}
   */
  isPerfectSquare(num) {
    return num ** 0.5 % 1 == 0;
  }
}
```

## Sqrt(x)

https://neetcode.io/problems/sqrtx/question

```js
class Solution {
  /**
   * @param {number} x
   * @return {number}
   */
  mySqrt(x) {
    let l = 0,
      r = x,
      m;
    while (l <= r) {
      m = Math.floor((l + r) / 2);
      if (m ** 2 == x) return m;
      [l, r] = m ** 2 < x ? [m + 1, r] : [l, m - 1];
    }
    return m ** 2 > x ? m - 1 : m;
  }
}
```

---

---

---

# Linked List

## Reverse Linked List

https://neetcode.io/problems/reverse-a-linked-list/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */

class Solution {
  /**
   * @param {ListNode} head
   * @return {ListNode}
   */
  reverseList(head) {
    let a = null;
    while (head) [head.next, a, head] = [a, head, head.next];
    return a;
  }
}
```

## Merge Two Sorted Linked Lists

https://neetcode.io/problems/merge-two-sorted-linked-lists/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */

class Solution {
  /**
   * @param {ListNode} list1
   * @param {ListNode} list2
   * @return {ListNode}
   */
  mergeTwoLists(list1, list2) {
    let n1 = list1,
      n2 = list2;
    let a = new ListNode();
    let n = a;
    while (n1 && n2) {
      [n.next, n1, n2] = n1.val < n2.val ? [n1, n1.next, n2] : [n2, n1, n2.next];
      n = n.next;
    }
    n.next = n1 || n2;
    return a.next;
  }
}
```

## Linked List Cycle Detection

https://neetcode.io/problems/linked-list-cycle-detection/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */

class Solution {
  /**
   * @param {ListNode} head
   * @return {boolean}
   */
  hasCycle(head) {
    let n1 = head,
      n2 = head;
    while (n2 && n2.next) {
      n1 = n1.next;
      n2 = n2.next.next;
      if (n1 === n2) return true;
    }
    return false;
  }
}
```

## Palindrome Linked List

https://neetcode.io/problems/palindrome-linked-list/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
class Solution {
  /**
   * @param {ListNode} head
   * @return {boolean}
   */
  isPalindrome(head) {
    let a = [],
      b = head;
    while (b) {
      a.push(b.val);
      b = b.next;
    }
    let l = 0,
      r = a.length - 1;
    while (l < r) if (a[l++] != a[r--]) return false;
    return true;
  }
}
```

## Remove Linked List Elements

https://neetcode.io/problems/remove-linked-list-elements/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
class Solution {
  /**
   * @param {ListNode} head
   * @param {number} val
   * @return {ListNode}
   */
  removeElements(head, val) {
    while (head && head.val == val) head = head.next;
    let a = head;
    while (a && a.next) {
      if (a.next.val == val) a.next = a.next.next;
      else a = a.next;
    }
    return head;
  }
}
```

## Remove Duplicates from Sorted List

https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

```js
/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
const deleteDuplicates = (head) => {
  let a = head;
  while (a && a.next) {
    if (a.val == a.next.val) a.next = a.next.next;
    else a = a.next;
  }
  return head;
};
```

## Middle of the Linked List

https://neetcode.io/problems/middle-of-the-linked-list/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
class Solution {
  /**
   * @param {ListNode} head
   * @return {ListNode}
   */
  middleNode(head) {
    let a = head,
      b = head;
    while (b && b.next) {
      a = a.next;
      b = b.next.next;
    }
    return a;
  }
}
```

## Intersection of Two Linked Lists

https://neetcode.io/problems/intersection-of-two-linked-lists/question

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
class Solution {
  /**
   * @param {ListNode} headA
   * @param {ListNode} headB
   * @return {ListNode}
   */
  getIntersectionNode(headA, headB) {
    let a = headA;
    while (a) {
      a.val = -a.val;
      a = a.next;
    }
    let b = headB,
      c = null;
    while (b && b.val > 0) b = b.next;
    c = b;
    while (b) {
      b.val = -b.val;
      b = b.next;
    }
    return c;
  }
}
```

```js
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     constructor(val = 0, next = null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
class Solution {
  /**
   * @param {ListNode} headA
   * @param {ListNode} headB
   * @return {ListNode}
   */
  getIntersectionNode(headA, headB) {
    let a = headA,
      b = headB;
    while (a !== b) {
      a = a ? a.next : headB;
      b = b ? b.next : headA;
    }
    return a;
  }
}
```

---

---

---

# Trees

## Binary Tree Inorder Traversal

https://neetcode.io/problems/binary-tree-inorder-traversal/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root
   * @return {number[]}
   */
  inorderTraversal(root) {
    const a = [];
    const dfs = (n) => {
      if (!n) return;
      dfs(n.left);
      a.push(n.val);
      dfs(n.right);
    };
    dfs(root);
    return a;
  }
}
```

## Binary Tree Preorder Traversal

https://neetcode.io/problems/binary-tree-preorder-traversal/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root
   * @return {number[]}
   */
  preorderTraversal(root) {
    const a = [];
    const dfs = (n) => {
      if (!n) return;
      a.push(n.val);
      dfs(n.left);
      dfs(n.right);
    };
    dfs(root);
    return a;
  }
}
```

## Binary Tree Postorder Traversal

https://neetcode.io/problems/binary-tree-postorder-traversal/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root
   * @return {number[]}
   */
  postorderTraversal(root) {
    const a = [];
    const dfs = (n) => {
      if (!n) return;
      dfs(n.left);
      dfs(n.right);
      a.push(n.val);
    };
    dfs(root);
    return a;
  }
}
```

## N-ary Tree Postorder Traversal

https://neetcode.io/problems/n-ary-tree-postorder-traversal/question

```js
/**
 * Definition for a binary tree node.
 * class Node {
 *     constructor(val = 0, children = []) {
 *         this.val = val;
 *         this.children = children;
 *     }
 * }
 */
class Solution {
  /**
   * @param {Node|null} root
   * @return {number[]}
   */
  postorder(root) {
    const a = [];
    const dfs = (n) => {
      if (!n) return;
      for (let i of n.children) dfs(i);
      a.push(n.val);
    };
    dfs(root);
    return a;
  }
}
```

## Invert Binary Tree

https://neetcode.io/problems/invert-a-binary-tree/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} root
   * @return {TreeNode}
   */
  invertTree(root) {
    const dfs = (n) => {
      if (!n) return;
      [n.left, n.right] = [n.right, n.left];
      dfs(n.left);
      dfs(n.right);
    };
    dfs(root);
    return root;
  }
}
```

## Maximum Depth of Binary Tree

https://neetcode.io/problems/depth-of-binary-tree/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} root
   * @return {number}
   */
  maxDepth(root) {
    let a0 = 0;
    const dfs = (n, a) => {
      if (!n) return;
      a++;
      a0 = a > a0 ? a : a0;
      dfs(n.left, a);
      dfs(n.right, a);
      return;
    };
    dfs(root, 0);
    return a0;
  }
}
```

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} root
   * @return {number}
   */
  maxDepth(n) {
    if (!n) return 0;
    const l = this.maxDepth(n.left);
    const r = this.maxDepth(n.right);
    return 1 + Math.max(l, r);
  }
}
```

## Diameter of Binary Tree

https://neetcode.io/problems/binary-tree-diameter/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} root
   * @return {number}
   */
  diameterOfBinaryTree(n) {
    let a = 0;
    const dfs = (n) => {
      if (!n) return 0;
      const l = dfs(n.left);
      const r = dfs(n.right);
      a = l + r > a ? l + r : a;
      return 1 + Math.max(l, r);
    };
    dfs(n);
    return a;
  }
}
```

## Balanced Binary Tree

https://neetcode.io/problems/balanced-binary-tree/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} root
   * @return {boolean}
   */
  isBalanced(n) {
    const dfs = (n) => {
      if (!n) return true;
      const l = dfs(n.left);
      if (!l) return false;
      const r = dfs(n.right);
      if (!r) return false;
      if (Math.abs(l - r) > 1) return false;
      return 1 + Math.max(l, r);
    };
    return dfs(n) > 0;
  }
}
```

## Same Binary Tree

https://neetcode.io/problems/same-binary-tree/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} p
   * @param {TreeNode} q
   * @return {boolean}
   */
  isSameTree(n1, n2) {
    const dfs = (n1, n2) => {
      if (!n1 && !n2) return true;
      if (!n1 || !n2) return false;
      const l = dfs(n1.left, n2.left);
      const r = dfs(n1.right, n2.right);
      return l && r && n1.val == n2.val;
    };
    return dfs(n1, n2);
  }
}
```

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} p
   * @param {TreeNode} q
   * @return {boolean}
   */
  isSameTree(n1, n2) {
    if (!n1 || !n2) return n1 === n2;
    return n1.val == n2.val && this.isSameTree(n1.left, n2.left) && this.isSameTree(n1.right, n2.right);
  }
}
```

## Subtree of Another Tree

https://neetcode.io/problems/subtree-of-a-binary-tree/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

class Solution {
  /**
   * @param {TreeNode} root
   * @param {TreeNode} subRoot
   * @return {boolean}
   */
  isSubtree(r0, r1) {
    const isSame = (n1, n2) => {
      if (!n1 || !n2) return n1 === n2;
      return n1.val === n2.val && isSame(n1.left, n2.left) && isSame(n1.right, n2.right);
    };

    const dfs = (n) => {
      if (!n) return false;
      if (isSame(n, r1)) return true;
      return dfs(n.left) || dfs(n.right);
    };
    return dfs(r0);
  }
}
```

## Convert Sorted Array to Binary Search Tree

https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {number[]} nums
 * @return {TreeNode}
 */
const sortedArrayToBST = (nums) => {
  const dfs = (l, r) => {
    if (l > r) return null;
    const m = (l + r) >> 1;
    return {
      val: nums[m],
      left: dfs(l, m - 1),
      right: dfs(m + 1, r),
    };
  };
  return dfs(0, nums.length - 1);
};
```

## Merge Two Binary Trees

https://neetcode.io/problems/merge-two-binary-trees/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root1
   * @param {TreeNode} root2
   * @return {TreeNode}
   */
  mergeTrees(root1, root2) {
    if (!root1) return root2;
    if (!root2) return root1;
    root1.val += root2.val;
    root1.left = this.mergeTrees(root1.left, root2.left);
    root1.right = this.mergeTrees(root1.right, root2.right);
    return root1;
  }
}
```

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root1
   * @param {TreeNode} root2
   * @return {TreeNode}
   */
  mergeTrees(root1, root2) {
    if (!root1 && !root2) return null;
    const n = new TreeNode((root1?.val ?? 0) + (root2?.val ?? 0));
    n.left = this.mergeTrees(root1?.left, root2?.left);
    n.right = this.mergeTrees(root1?.right, root2?.right);
    return n;
  }
}
```

## Path Sum

https://neetcode.io/problems/path-sum/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root
   * @param {number} targetSum
   * @return {boolean}
   */
  hasPathSum(root, targetSum) {
    const dfs = (n, s) => {
      if (!n) return false;
      s += n.val;
      if (!n.left && !n.right) return s == targetSum;
      return dfs(n.left, s) || dfs(n.right, s);
    };
    return dfs(root, 0);
  }
}
```

## Range Sum of BST

https://neetcode.io/problems/range-sum-of-bst/question

```js
/**
 * Definition for a binary tree node.
 * class TreeNode {
 *     constructor(val = 0, left = null, right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
  /**
   * @param {TreeNode} root
   * @param {number} low
   * @param {number} high
   * @return {number}
   */
  rangeSumBST(root, low, high) {
    let a = 0;
    const dfs = (n) => {
      if (!n) return;
      if (n.val >= low && n.val <= high) a += n.val;
      dfs(n.left);
      dfs(n.right);
    };
    dfs(root, low, high);
    return a;
  }
}
```

## Leaf-Similar Trees

https://leetcode.com/problems/leaf-similar-trees/description/

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root1
 * @param {TreeNode} root2
 * @return {boolean}
 */
const leafSimilar = (root1, root2) => {
  const fn = (n, a) => {
    if (!n) return;
    if (!n.left && !n.right) {
      a.push(n.val);
      return;
    }
    fn(n.left, a);
    fn(n.right, a);
  };

  const a1 = [];
  fn(root1, a1);
  const a2 = [];
  fn(root2, a2);
  return a1.join(',') == a2.join(',');
};
```

## Evaluate Boolean Binary Tree

https://leetcode.com/problems/evaluate-boolean-binary-tree/description/

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {boolean}
 */
const evaluateTree = (root) => {
  const a = [];
  const dfs = (n) => {
    if (!n) return;
    dfs(n.left);
    dfs(n.right);
    if (n.val == 0 || n.val == 1) {
      a.push(n.val);
    } else {
      const r = a.pop();
      const l = a.pop();
      a.push(n.val == 2 ? l || r : l && r);
    }
  };
  dfs(root);
  return a[0];
};
```

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {boolean}
 */
const evaluateTree = (n) => {
  if (!n.left && !n.right) return n.val;
  const l = evaluateTree(n.left);
  const r = evaluateTree(n.right);
  if (n.val == 2) return l || r;
  if (n.val == 3) return l && r;
};
```

## Minimum Distance Between BST Nodes

https://leetcode.com/problems/minimum-distance-between-bst-nodes/description/

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {number}
 */
const minDiffInBST = (root) => {
  let a = -Infinity,
    b = Infinity;
  const dfs = (n) => {
    if (!n) return;
    dfs(n.left);
    b = n.val - a < b ? n.val - a : b;
    a = n.val;
    dfs(n.right);
  };
  dfs(root);
  return b;
};
```

## Symmetric Tree

https://leetcode.com/problems/symmetric-tree/description/

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {boolean}
 */
const isSymmetric = (root) => {
  const dfs1 = (n) => {
    if (!n) {
      a1.push(null);
      return;
    }
    a1.push(n.val);
    dfs1(n.left);
    dfs1(n.right);
  };
  let a1 = [];
  dfs1(root.left);

  const dfs2 = (n) => {
    if (!n) {
      a2.push(null);
      return;
    }
    a2.push(n.val);
    dfs2(n.right);
    dfs2(n.left);
  };
  let a2 = [];
  dfs2(root.right);

  return a1.join(',') == a2.join(',');
};
```

```js
/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {boolean}
 */
const isSymmetric = (root) => {
  const dfs = (l, r) => {
    if (!l && !r) return true;
    if (!l || !r) return false;
    if (l.val !== r.val) return false;
    return dfs(l.left, r.right) && dfs(l.right, r.left);
  };
  return dfs(root.left, root.right);
};
```

---

---

---

# Trie

## Count Prefix and Suffix Pairs I

https://neetcode.io/problems/count-prefix-and-suffix-pairs-i/question

```js
class Solution {
  /**
   * @param {string[]} words
   * @return {number}
   */
  isPrefixAndSuffix(str1, str2) {
    const n = str1.length;
    return str2.slice(0, n) == str1 && str2.slice(-n) == str1;
  }

  countPrefixSuffixPairs(words) {
    let a = 0;
    for (let i = 0; i < words.length - 1; i++) {
      for (let j = i + 1; j < words.length; j++) {
        a += this.isPrefixAndSuffix(words[i], words[j]) ? 1 : 0;
      }
    }
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {string[]} words
   * @return {number}
   */
  countPrefixSuffixPairs(words) {
    const map = new Map();
    let res = 0;
    for (const w of words) {
      const n = w.length;
      for (let len = 1; len <= n; len++) {
        const pre = w.slice(0, len);
        const suf = w.slice(n - len);
        if (pre == suf && map.has(pre)) {
          res += map.get(pre);
        }
      }
      map.set(w, (map.get(w) || 0) + 1);
    }
    return res;
  }
}
```

## Counting Words With a Given Prefix

https://neetcode.io/problems/counting-words-with-a-given-prefix/question

```js
class Solution {
  /**
   * @param {string[]} words
   * @param {string} pref
   * @return {number}
   */
  prefixCount(words, pref) {
    const re = new RegExp('^' + pref);
    let a = 0;
    for (let i of words) a = re.test(i) ? a + 1 : a;
    return a;
  }
}
```

---

---

---

# Heap/Priority Queue

## Kth Largest Element in a Stream

https://neetcode.io/problems/kth-largest-integer-in-a-stream/question

```js
class KthLargest {
  /**
   * @param {number} k
   * @param {number[]} nums
   */
  constructor(k, nums) {
    this.k = k;
    this.nums = nums;
  }

  /**
   * @param {number} val
   * @return {number}
   */
  add(val) {
    this.nums.push(val);
    this.nums.sort((x1, x2) => x2 - x1).slice(0, this.k);
    return this.nums[this.k - 1];
  }
}
```

## Last Stone Weight

https://neetcode.io/problems/last-stone-weight/question

```js
class Solution {
  /**
   * @param {number[]} stones
   * @return {number}
   */
  lastStoneWeight(stones) {
    while (stones.length > 1) {
      stones.sort((x1, x2) => x1 - x2);
      const x = stones.pop();
      const y = stones.pop();
      if (x == y) continue;
      stones.push(Math.abs(x - y));
    }
    return stones[0] || 0;
  }
}
```

## Take Gifts From the Richest Pile

https://neetcode.io/problems/take-gifts-from-the-richest-pile/question

```js
class Solution {
  /**
   * @param {number[]} gifts
   * @param {number} k
   * @return {number}
   */
  pickGifts(gifts, k) {
    for (let i = 0; i < k; i++) {
      const ii = gifts.indexOf(Math.max(...gifts));
      gifts[ii] = Math.floor(gifts[ii] ** 0.5);
    }
    return gifts.reduce((a, x) => a + x, 0);
  }
}
```

## Final Array State After K Multiplication Operations I

https://neetcode.io/problems/final-array-state-after-k-multiplication-operations-i/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @param {number} multiplier
   * @return {number[]}
   */
  getFinalState(nums, k, multiplier) {
    for (let i = 0; i < k; i++) {
      const ii = nums.indexOf(Math.min(...nums));
      nums[ii] = nums[ii] * multiplier;
    }
    return nums;
  }
}
```

---

---

---

# Intervals

## Meeting Rooms

https://neetcode.io/problems/meeting-schedule/question

```js
/**
 * Definition of Interval:
 * class Interval {
 *   constructor(start, end) {
 *     this.start = start;
 *     this.end = end;
 *   }
 * }
 */

class Solution {
  /**
   * @param {Interval[]} intervals
   * @returns {boolean}
   */
  canAttendMeetings(intervals) {
    let a = [];
    for (const { start: s0, end: e0 } of intervals) {
      for (const [s, e] of a) {
        if (s0 < e && e0 > s) return false;
      }
      a.push([s0, e0]);
    }
    return true;
  }
}
```

```js
/**
 * Definition of Interval:
 * class Interval {
 *   constructor(start, end) {
 *     this.start = start;
 *     this.end = end;
 *   }
 * }
 */

class Solution {
  /**
   * @param {Interval[]} intervals
   * @returns {boolean}
   */
  canAttendMeetings(intervals) {
    intervals.sort((x1, x2) => x1.start - x2.start);
    for (let i = 1; i < intervals.length; i++) {
      if (intervals[i].start < intervals[i - 1].end) return false;
    }
    return true;
  }
}
```

---

---

---

# Greedy

## Buy Two Chocolates

https://neetcode.io/problems/buy-two-chocolates/question

```js
class Solution {
  /**
   * @param {number[]} prices
   * @param {number} money
   * @return {number}
   */
  buyChoco(prices, money) {
    prices.sort((x1, x2) => x1 - x2);
    const a = prices[0] + prices[1];
    return money < a ? money : money - a;
  }
}
```

## Lemonade Change

https://neetcode.io/problems/lemonade-change/question

```js
class Solution {
  /**
   * @param {number[]} bills
   * @return {boolean}
   */
  lemonadeChange(bills) {
    let a05 = 0,
      a10 = 0,
      a20 = 0;
    for (let i of bills) {
      if (i == 5) {
        a05++;
      } else if (i == 10) {
        (a05--, a10++);
      } else {
        if (a10 > 0) {
          (a05--, a10--);
        } else {
          a05 -= 3;
        }
      }
      if (a05 < 0) return false;
    }
    return true;
  }
}
```

## Minimum Number of Moves to Seat Everyone

https://neetcode.io/problems/minimum-number-of-moves-to-seat-everyone/question

```js
class Solution {
  /**
   * @param {number[]} seats
   * @param {number[]} students
   * @return {number}
   */
  minMovesToSeat(seats, students) {
    seats.sort((x1, x2) => x1 - x2);
    students.sort((x1, x2) => x1 - x2);
    let a = 0;
    for (let i = 0; i < seats.length; i++) a += Math.abs(seats[i] - students[i]);
    return a;
  }
}
```

## Maximum Odd Binary Number

https://neetcode.io/problems/maximum-odd-binary-number/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {string}
   */
  maximumOddBinaryNumber(s) {
    return s.replaceAll('0', '').slice(1) + s.replaceAll('1', '') + '1';
  }
}
```

## Maximum Nesting Depth of the Parentheses

https://neetcode.io/problems/maximum-nesting-depth-of-the-parentheses/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  maxDepth(s) {
    let a = 0,
      b = 0;
    for (let i of [...s]) {
      if (i == '(') b++;
      else if (i == ')') b--;
      a = b > a ? b : a;
    }
    return a;
  }
}
```

## Check if One String Swap Can Make Strings Equal

https://leetcode.com/problems/check-if-one-string-swap-can-make-strings-equal/description/

```js
/**
 * @param {string} s1
 * @param {string} s2
 * @return {boolean}
 */
const areAlmostEqual = (s1, s2) => {
  if (s1 == s2) return true;
  for (let i1 = 0; i1 < s1.length - 1; i1++) {
    for (let i2 = i1 + 1; i2 < s1.length; i2++) {
      let s = [...s1];
      [s[i1], s[i2]] = [s[i2], s[i1]];
      if (s.join('') == s2) return true;
    }
  }
  return false;
};
```

## Make Two Arrays Equal by Reversing Subarrays

https://leetcode.com/problems/make-two-arrays-equal-by-reversing-subarrays/description/

```js
/**
 * @param {number[]} target
 * @param {number[]} arr
 * @return {boolean}
 */
const canBeEqual = (target, arr) => {
  return target.sort().join(',') == arr.sort().join(',');
};
```

```js
/**
 * @param {number[]} target
 * @param {number[]} arr
 * @return {boolean}
 */
const canBeEqual = (target, arr) => {
  let a = {};
  for (let i of target) a[i] = (a[i] ?? 0) + 1;
  for (let i of arr) {
    if (!a[i]) return false;
    a[i]--;
  }
  return true;
};
```

---

---

---

# Back Tracking

## Sum of All Subsets XOR Total

https://neetcode.io/problems/sum-of-all-subset-xor-totals/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  subsetXORSum(nums) {
    let a = 0;
    for (let i of nums) a |= i;
    return a << (nums.length - 1);
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  subsetXORSum(nums) {
    const dfs = (i, x) => (i == nums.length ? x : dfs(i + 1, x ^ nums[i]) + dfs(i + 1, x));

    return dfs(0, 0);
  }
}
```

---

---

---

# Graphs

## Island Perimeter

https://neetcode.io/problems/island-perimeter/question

```js
class Solution {
    /**
     * @param {number[][]} grid
     * @return {number}
     */
    islandPerimeter(grid) {
        const x=grid[0].length+2;
        const y=grid.length+2;
        let a=[Array(x).fill(0)];
        for(let i=0;i<y-2;i++) a.push([0,...grid[i],0]);
        a.push(Array(x).fill(0));
        let b=0;
        for(let i=1;i<y-1;i++){
            for(let j=1;j<x-1;j++){
                if(a[i][j]==1){
                    if(a[i][j-1]==0) b++;
                    if(a[i][j+1]==0) b++;
                    if(a[i-1][j]==0) b++;
                    if(a[i+1][j]==0) b++;
                }
            }
        }
        return b;
}
```

```js
class Solution {
  /**
   * @param {number[][]} grid
   * @return {number}
   */
  islandPerimeter(grid) {
    let a = 0,
      b = 0;
    for (let i = 0; i < grid.length; i++) {
      for (let j = 0; j < grid[0].length; j++) {
        if (grid[i][j] == 1) {
          a++;
          if (i > 0 && grid[i - 1][j] == 1) b++;
          if (j > 0 && grid[i][j - 1] == 1) b++;
        }
      }
    }
    return a * 4 - b * 2;
  }
}
```

## Verifying An Alien Dictionary

https://neetcode.io/problems/verifying-an-alien-dictionary/question

```js
class Solution {
  /**
   * @param {string[]} words
   * @param {string} order
   * @return {boolean}
   */
  isAlienSorted(words, order) {
    let a = {};
    for (let i = 0; i < 26; i++) a[order[i]] = String.fromCharCode(97 + i);
    //console.log(a);
    let b0 = '';
    for (let i of words) {
      let b = '';
      for (let j of i) b += a[j];
      if (b < b0) return false;
      b0 = b;
    }
    return true;
  }
}
```

## Find the Town Judge

https://neetcode.io/problems/find-the-town-judge/question

```js
class Solution {
  /**
   * @param {number} n
   * @param {number[][]} trust
   * @return {number}
   */
  findJudge(n, trust) {
    let c = Array(n + 1).fill(0);
    for (let [a, b] of trust) {
      c[a]--;
      c[b]++;
    }
    return c.findIndex((x) => x == n - 1);
  }
}
```

## Flood Fill

https://neetcode.io/problems/flood-fill/question

```js
class Solution {
  /**
   * @param {number[][]} image
   * @param {number} sr
   * @param {number} sc
   * @param {number} color
   * @return {number[][]}
   */
  floodFill(image, sr, sc, color) {
    const m = image.length;
    const n = image[0].length;
    const org = image[sr][sc];
    if (org == color) return image;
    let vst = Array.from({ length: m }, () => Array(n).fill(false));
    let que = [];

    const bfs = (y, x) => {
      image[y][x] = color;
      vst[y][x] = true;
      que.push([y, x]);
    };

    bfs(sr, sc);
    while (que.length) {
      const [y, x] = que.pop();
      if (y > 0 && !vst[y - 1][x] && image[y - 1][x] == org) bfs(y - 1, x);
      if (y < m - 1 && !vst[y + 1][x] && image[y + 1][x] == org) bfs(y + 1, x);
      if (x > 0 && !vst[y][x - 1] && image[y][x - 1] == org) bfs(y, x - 1);
      if (x < n - 1 && !vst[y][x + 1] && image[y][x + 1] == org) bfs(y, x + 1);
    }
    return image;
  }
}
```

```js
class Solution {
  /**
   * @param {number[][]} image
   * @param {number} sr
   * @param {number} sc
   * @param {number} color
   * @return {number[][]}
   */
  floodFill(image, sr, sc, color) {
    const m = image.length;
    const n = image[0].length;
    const org = image[sr][sc];
    if (org == color) return image;
    const dfs = (y, x) => {
      if (y < 0 || x < 0 || y >= m || x >= n) return;
      if (image[y][x] != org) return;
      image[y][x] = color;
      dfs(y + 1, x);
      dfs(y - 1, x);
      dfs(y, x + 1);
      dfs(y, x - 1);
    };

    dfs(sr, sc);
    return image;
  }
}
```

---

---

---

# 1-D DP

## Climbing Stairs

https://neetcode.io/problems/climbing-stairs/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  climbStairs(n) {
    if (n == 1) return 1;
    let dp = [];
    ((dp[0] = 1), (dp[1] = 1));
    for (let i = 2; i <= n; i++) dp[i] = dp[i - 1] + dp[i - 2];
    return dp[n];
  }
}
```

```js
class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  climbStairs(n) {
    let a = 1,
      b = 1;
    for (let i = 2; i <= n; i++) [a, b] = [b, b + a];
    return b;
  }
}
```

## Min Cost Climbing Stairs

https://neetcode.io/problems/min-cost-climbing-stairs/question

```js
class Solution {
  /**
   * @param {number[]} cost
   * @return {number}
   */
  minCostClimbingStairs(cost) {
    const n = cost.length;
    let dp = [];
    ((dp[0] = 0), (dp[1] = 0));
    for (let i = 2; i <= n; i++) {
      dp[i] = Math.min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
    }
    return dp[n];
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} cost
   * @return {number}
   */
  minCostClimbingStairs(cost) {
    let a = 0,
      b = 0;
    for (let i = 2; i <= cost.length; i++) {
      [a, b] = [b, Math.min(b + cost[i - 1], a + cost[i - 2])];
    }
    return b;
  }
}
```

## N-th Tribonacci Number

https://neetcode.io/problems/n-th-tribonacci-number/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  tribonacci(n) {
    let dp = [];
    ((dp[0] = 0), (dp[1] = 1), (dp[2] = 1));
    for (let i = 3; i <= n; i++) dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3];
    return dp[n];
  }
}
```

```js
class Solution {
  /**
   * @param {number} n
   * @return {number}
   */
  tribonacci(n) {
    if (n == 0) return 0;
    let a = 0,
      b = 1,
      c = 1;
    for (let i = 3; i <= n; i++) [a, b, c] = [b, c, a + b + c];
    return c;
  }
}
```

---

---

---

# Bit Manupulation

## Single Number

https://neetcode.io/problems/single-number/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  singleNumber(nums) {
    let a = 0;
    for (let i of nums) a ^= i;
    return a;
  }
}
```

## Number of 1 Bits

https://neetcode.io/problems/number-of-one-bits/question

```js
class Solution {
  /**
   * @param {number} n - a positive integer
   * @return {number}
   */
  hammingWeight(n) {
    let a = 0;
    while (n) {
      n &= n - 1;
      a++;
    }
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number} n - a positive integer
   * @return {number}
   */
  hammingWeight(n) {
    let a = 0;
    while (n) {
      a += n & 1;
      n >>= 1;
    }
    return a;
  }
}
```

## Counting Bits

https://neetcode.io/problems/counting-bits/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {number[]}
   */
  countBits(n) {
    let a = [];
    for (let i = 0; i <= n; i++) {
      let b = i,
        c = 0;
      while (b) {
        b &= b - 1;
        c++;
      }
      a.push(c);
    }
    return a;
  }
}
```

## Add Binary

https://neetcode.io/problems/add-binary/question

```js
class Solution {
  /**
   * @param {string} a
   * @param {string} b
   * @return {string}
   */
  addBinary(a, b) {
    a = Array.from(a).map(Number).reverse();
    b = Array.from(b).map(Number).reverse();
    let c = [],
      d = 0;

    for (let i = 0; i < Math.max(a.length, b.length); i++) {
      const ai = a[i] ?? 0;
      const bi = b[i] ?? 0;
      c[i] = ai ^ bi ^ d;
      d = ai & bi || ai & d || bi & d;
    }
    if (d) c.push(d);
    return c.reverse().join('');
  }
}
```

```js
class Solution {
  /**
   * @param {string} a
   * @param {string} b
   * @return {string}
   */
  addBinary(a, b) {
    return (BigInt('0b' + a) + BigInt('0b' + b)).toString(2);
  }
}
```

## Minimum Bit Flips to Convert Number

https://leetcode.com/problems/minimum-bit-flips-to-convert-number/description/

```js
/**
 * @param {number} start
 * @param {number} goal
 * @return {number}
 */
const minBitFlips = (start, goal) => {
  let a = start ^ goal,
    b = 0;
  while (a) [a, b] = [a & (a - 1), b + 1];
  return b;
};
```

## Reverse Bits

https://neetcode.io/problems/reverse-bits/question

```js
class Solution {
  /**
   * @param {number} n - a positive integer
   * @return {number} - a positive integer
   */
  reverseBits(n) {
    let a = n.toString(2).padStart(32, '0');
    a = Array.from(a).reverse().join('');
    return Number('0b' + a);
  }
}
```

## Missing Number

https://neetcode.io/problems/missing-number/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  missingNumber(nums) {
    for (let i = 0; i <= nums.length; i++) {
      if (nums.indexOf(i) == -1) return i;
    }
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  missingNumber(nums) {
    let a = 0;
    for (let i = 1; i <= nums.length; i++) a ^= i;
    for (let i of nums) a ^= i;
    return a;
  }
}
```

## Shuffle the Array

https://leetcode.com/problems/shuffle-the-array/description/

```js
/**
 * @param {number[]} nums
 * @param {number} n
 * @return {number[]}
 */
const shuffle = (nums, n) => {
  let a = [];
  for (let i = 0; i < n; i++) {
    a.push(nums[i]);
    a.push(nums[n + i]);
  }
  return a;
};
```

## Add to Array-Form of Integer

https://leetcode.com/problems/add-to-array-form-of-integer/description/

```js
/**
 * @param {number[]} num
 * @param {number} k
 * @return {number[]}
 */
const addToArrayForm = (num, k) => {
  const a = BigInt(num.join(''));
  const b = BigInt(k);
  return [...String(a + b)].map(Number);
};
```

```js
/**
 * @param {number[]} num
 * @param {number} k
 * @return {number[]}
 */
const addToArrayForm = (num, k) => {
  let i = num.length - 1;
  while (k > 0 || i >= 0) {
    if (i >= 0) {
      k += num[i];
      num[i] = k % 10;
      i--;
    } else {
      num.unshift(k % 10);
    }
    k = (k / 10) | 0;
  }
  return num;
};
```

## Find the Difference

https://neetcode.io/problems/find-the-difference/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {character}
   */
  findTheDifference(s, t) {
    let a = {};
    for (let i of s) a[i] = (a[i] ?? 0) + 1;
    for (let i of t) {
      if (!a[i]) return i;
      a[i]--;
    }
  }
}
```

## Power of Two

https://neetcode.io/problems/power-of-two/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {boolean}
   */
  isPowerOfTwo(n) {
    return Number.isInteger(Math.log2(n));
  }
}
```

---

---

---

# Math & Geometry

## Excel Sheet Column Title

https://neetcode.io/problems/excel-sheet-column-title/question

```js
class Solution {
  /**
   * @param {number} columnNumber
   * @return {string}
   */
  convertToTitle(columnNumber) {
    let n = columnNumber;
    let a = '';
    while (n > 0) {
      n--;
      a = String.fromCharCode((n % 26) + 65) + a;
      n = Math.floor(n / 26);
    }
    return a;
  }
}
```

## Greatest Common Divisor of Strings

https://neetcode.io/problems/greatest-common-divisor-of-strings/question

```js
class Solution {
  /**
   * @param {string} str1
   * @param {string} str2
   * @return {string}
   */
  gcdOfStrings(str1, str2) {
    let a = 0,
      b;
    if (str2.length > str1.length) [str2, str1] = [str1, str2];
    while (true) {
      a++;
      b = str2.slice(0, str2.length / a);
      if (str1.split(b).join('') == '' || b == '') return b;
    }
  }
}
```

## Count Odd Numbers in an Interval Range

https://neetcode.io/problems/count-odd-numbers-in-an-interval-range/question

```js
class Solution {
  /**
   * @param {number} low
   * @param {number} high
   * @return {number}
   */
  countOdds(low, high) {
    return ((high + 1) >> 1) - (low >> 1);
  }
}
```

## Matrix Diagonal Sum

https://neetcode.io/problems/matrix-diagonal-sum/question

```js
class Solution {
  /**
   * @param {number[][]} mat
   * @return {number}
   */
  diagonalSum(mat) {
    const n = mat.length;
    let a = 0;
    for (let i = 0; i < n; i++) {
      a += mat[i][i] + mat[i][n - i - 1];
    }
    if (n % 2) a -= mat[n >> 1][n >> 1];
    return a;
  }
}
```

## Calculate Money in Leetcode Bank

https://leetcode.com/problems/calculate-money-in-leetcode-bank/description/

```js
/**
 * @param {number} n
 * @return {number}
 */
const totalMoney = (n) => {
  const w = Math.floor(n / 7),
    d = n % 7;
  return 28 * w + (7 * w * (w - 1)) / 2 + d * w + (d * (d + 1)) / 2;
};
```

## Largest Odd Number in String

https://leetcode.com/problems/largest-odd-number-in-string/description/

```js
/**
 * @param {string} num
 * @return {string}
 */
const largestOddNumber = (num) => {
  let n = num.length;
  while (n > 0) {
    if (num.at(n - 1) % 2 != 0) break;
    n--;
  }
  return num.slice(0, n);
};
```

## Transpose Matrix

https://neetcode.io/problems/transpose-matrix/question

```js
class Solution {
  /**
   * @param {number[][]} matrix
   * @return {number[][]}
   */
  transpose(matrix) {
    let a = new Array(matrix[0].length);
    for (let i = 0; i < a.length; i++) a[i] = [];

    for (let i = 0; i < matrix.length; i++) {
      for (let j = 0; j < matrix[0].length; j++) a[j][i] = matrix[i][j];
    }
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number[][]} matrix
   * @return {number[][]}
   */
  transpose(matrix) {
    return matrix[0].map((_, c) => matrix.map((r) => r[c]));
  }
}
```

## Image Smoother

https://leetcode.com/problems/image-smoother/description/

```js
/**
 * @param {number[][]} img
 * @return {number[][]}
 */
const imageSmoother = (img) => {
  const m = img.length,
    n = img[0].length;
  let a = Array.from({ length: m }, () => Array(n));
  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      let b = 0,
        c = 0;
      for (let ii = -1; ii <= 1; ii++) {
        for (let jj = -1; jj <= 1; jj++) {
          if (i + ii < 0 || i + ii > m - 1 || j + jj < 0 || j + jj > n - 1) continue;
          b += img[i + ii][j + jj];
          c++;
        }
      }
      a[i][j] = (b / c) | 0;
    }
  }
  return a;
};
```

## Count of Matches in Tournament

https://leetcode.com/problems/count-of-matches-in-tournament/description/

```js
/**
 * @param {number} n
 * @return {number}
 */
const numberOfMatches = (n) => {
  let a = 0;
  while (n > 1) {
    if (n % 2 == 0) [a, n] = [a + n / 2, n / 2];
    else [a, n] = [a + (n - 1) / 2, (n - 1) / 2 + 1];
  }
  return a;
};
```

```js
/**
 * @param {number} n
 * @return {number}
 */
const numberOfMatches = (n) => n - 1;
```

## Water Bottles

https://leetcode.com/problems/water-bottles/description/

```js
/**
 * @param {number} numBottles
 * @param {number} numExchange
 * @return {number}
 */
const numWaterBottles = (numBottles, numExchange) => {
  let a = numBottles,
    b = a;
  while (b >= numExchange) {
    const c = (b / numExchange) | 0;
    a += c;
    b = c + (b % numExchange);
  }
  return a;
};
```

```js
/**
 * @param {number} numBottles
 * @param {number} numExchange
 * @return {number}
 */
const numWaterBottles = (numBottles, numExchange) => {
  return (numBottles + (numBottles - 1) / (numExchange - 1)) | 0;
};
```

## Largest Local Values in a Matrix

https://leetcode.com/problems/largest-local-values-in-a-matrix/description/

```js
/**
 * @param {number[][]} grid
 * @return {number[][]}
 */
const largestLocal = (grid) => {
  const n = grid.length;
  let a = [...Array(n)].map(() => Array(n - 2));
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - 2; j++) {
      a[i][j] = Math.max(grid[i][j], grid[i][j + 1], grid[i][j + 2]);
    }
  }
  let b = [...Array(n - 2)].map(() => Array(n - 2));
  for (let j = 0; j < n - 2; j++) {
    for (let i = 0; i < n - 2; i++) {
      b[i][j] = Math.max(a[i][j], a[i + 1][j], a[i + 2][j]);
    }
  }
  return b;
};
```

```js
/**
 * @param {number[][]} grid
 * @return {number[][]}
 */
const largestLocal = (grid) => {
  const n = grid.length;
  const a = Array.from({ length: n - 2 }, () => Array(n - 2).fill(0));
  for (let i = 0; i < n - 2; i++) {
    for (let j = 0; j < n - 2; j++) {
      let b = 0;
      for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) b = Math.max(b, grid[i + x][j + y]);
      }
      a[i][j] = b;
    }
  }
  return a;
};
```

## Power of Four

https://leetcode.com/problems/power-of-four/description/

```js
/**
 * @param {number} n
 * @return {boolean}
 */
const isPowerOfFour = (n) => Number.isInteger(Math.log2(n) / 2);
```

## Lucky Numbers in a Matrix

https://leetcode.com/problems/lucky-numbers-in-a-matrix/description/

```js
/**
 * @param {number[][]} matrix
 * @return {number[]}
 */
const luckyNumbers = (matrix) => {
  const m = matrix.length;
  const n = matrix[0].length;
  let a = [];
  for (let i = 0; i < m; i++) {
    const c = Math.min(...matrix[i]);
    a.push(matrix[i].indexOf(c));
  }
  let b = [];
  for (let j = 0; j < n; j++) {
    let c = -Infinity,
      d;
    for (let i = 0; i < m; i++) {
      if (matrix[i][j] > c) [c, d] = [matrix[i][j], i];
    }
    b.push(d);
  }
  let c = [];
  for (let i = 0; i < m; i++) {
    if (b[a[i]] == i) c.push(matrix[i][a[i]]);
  }
  return c;
};
```

```js
/**
 * @param {number[][]} matrix
 * @return {number[]}
 */
const luckyNumbers = (matrix) => {
  const m = matrix.length;
  const n = matrix[0].length;
  const a = [];
  for (let i = 0; i < m; i++) {
    const b = Math.min(...matrix[i]);
    const c = matrix[i].indexOf(b);
    let d = true;
    for (let k = 0; k < m; k++) {
      if (matrix[k][c] > b) {
        d = false;
        break;
      }
    }
    if (d) a.push(b);
  }
  return a;
};
```

## Non-Cyclical Number

https://neetcode.io/problems/non-cyclical-number/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {boolean}
   */
  isHappy(n) {
    let a = [];
    while (true) {
      const arr = Array.from(n + '');
      const b = arr.map((x) => x ** 2).reduce((x, a) => x + a);
      if (b == 1) return true;
      if (a.indexOf(b) != -1) return false;
      a.push(b);
      n = b;
    }
  }
}
```

## Plus One

https://neetcode.io/problems/plus-one/question

```js
class Solution {
  /**
   * @param {number[]} digits
   * @return {number[]}
   */
  plusOne(digits) {
    const a = digits.join('') * 1 + 1;
    return Array.from(a + '').map(Number);
  }
}
```

## Palindrome Number

https://neetcode.io/problems/palindrome-number/question

```js
class Solution {
  /**
   * @param {number} x
   * @return {boolean}
   */
  isPalindrome(x) {
    if (x < 0) return false;
    return [...(x + '')].reverse().join('') == x + '';
  }
}
```

## Ugly Number

https://neetcode.io/problems/ugly-number/question

```js
class Solution {
  /**
   * @param {number} n
   * @return {boolean}
   */
  isUgly(n) {
    if (n <= 0) return false;
    while (n > 1) {
      const a = n;
      if (n % 2 == 0) n /= 2;
      if (n % 3 == 0) n /= 3;
      if (n % 5 == 0) n /= 5;
      if (n == a) return false;
    }
    return true;
  }
}
```

## Convert 1D Array Into 2D Array

https://leetcode.com/problems/convert-1d-array-into-2d-array/description/

```js
/**
 * @param {number[]} original
 * @param {number} m
 * @param {number} n
 * @return {number[][]}
 */
const construct2DArray = (original, m, n) => {
  const l = original.length;
  if (l != m * n) return [];
  let a = Array.from({ length: m }, () => Array(n));
  for (let i = 0; i < l; i++) a[(i / n) | 0][i % n] = original[i];
  return a;
};
```

```js
/**
 * @param {number[]} original
 * @param {number} m
 * @param {number} n
 * @return {number[][]}
 */
const construct2DArray = (original, m, n) =>{
  return original.length !== m * n
    ? []
    : Array.from({ length: m }, (_, i) => original.slice(i * n, i * n + n)));
}
```

## Shift 2D Grid

https://leetcode.com/problems/shift-2d-grid/description/

```js
/**
 * @param {number[][]} grid
 * @param {number} k
 * @return {number[][]}
 */
const shiftGrid = (grid, k) => {
  const m = grid.length;
  const n = grid[0].length;
  grid = grid.flat();
  for (let i = 0; i < k; i++) grid.unshift(grid.pop());
  let a = [];
  for (let i = 0; i < m; i++) a[i] = grid.slice(i * n, i * n + n);
  return a;
};
```

## Roman to Integer

https://neetcode.io/problems/roman-to-integer/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  romanToInt(s) {
    let a = Array.from(s);
    let b = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };
    let c = 0;
    while (a.length > 0) {
      const d = a.pop();
      c += b[d];
      if (c >= 500) {
        b.C = -100;
      } else if (c >= 50) {
        b.X = -10;
      } else if (c >= 5) {
        b.I = -1;
      }
    }
    return c;
  }
}
```

## Widest Vertical Area Between Two Points Containing No Points

https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points/description/

```js
/**
 * @param {number[][]} points
 * @return {number}
 */
const maxWidthOfVerticalArea = (points) => {
  const n = points.length;
  let a = [];
  for (let i = 0; i < n; i++) a.push(points[i][0]);
  a.sort((x1, x2) => x1 - x2);
  let b = 0;
  for (let i = 1; i < n; i++) b = a[i] - a[i - 1] > b ? a[i] - a[i - 1] : b;
  return b;
};
```

---

---

---

# Medium Problems

# Javascript

## Memorize

https://leetcode.com/problems/memoize/description/

```js
/**
 * @param {Function} fn
 * @return {Function}
 */
function memoize(fn) {
  let a = {};
  return function (...args) {
    const b = args.toString();
    if (b in a) return a[b];
    a[b] = fn(...args);
    return a[b];
  };
}
/**
 * let callCount = 0;
 * const memoizedFn = memoize(function (a, b) {
 *	 callCount += 1;
 *   return a + b;
 * })
 * memoizedFn(2, 3) // 5
 * memoizedFn(2, 3) // 5
 * console.log(callCount) // 1
 */
```

## Cache with Time Limit

https://leetcode.com/problems/cache-with-time-limit/description/

```js
class TimeLimitedCache {
  constructor() {
    this.m = new Map();
  }

  /**
   * @param {number} key
   * @param {number} value
   * @param {number} duration
   * @return {boolean}
   */
  set(key, value, duration) {
    const now = Date.now();
    const exist = this.m.has(key) && this.m.get(key)[1] > now;
    this.m.set(key, [value, now + duration]);
    return exist;
  }

  /**
   * @param {number} key
   * @return {number}
   */
  get(key) {
    const v = this.m.get(key);
    return v && v[1] > Date.now() ? v[0] : -1;
  }

  /**
   * @return {number}
   */
  count() {
    const now = Date.now();
    let c = 0;
    for (const [, exp] of this.m.values()) {
      if (exp > now) c++;
    }
    return c;
  }
}
```

## Debounce

https://leetcode.com/problems/debounce/description/

```js
/**
 * @param {Function} fn
 * @param {number} t milliseconds
 * @return {Function}
 */
const debounce = (fn, t) => {
  let id;
  return (...args) => {
    clearTimeout(id);
    id = setTimeout(fn, t, ...args);
  };
};

/**
 * const log = debounce(console.log, 100);
 * log('Hello'); // cancelled
 * log('Hello'); // cancelled
 * log('Hello'); // Logged at t=100ms
 */
```

## Flatten Deeply Nested Array

https://leetcode.com/problems/flatten-deeply-nested-array/description/

```js
/**
 * @param {Array} arr
 * @param {number} depth
 * @return {Array}
 */
const flat = (arr, n) => {
  let a = arr.map((x) => [x, n]).reverse();
  let b = [];
  while (a.length) {
    const [v, d] = a.pop();
    if (Array.isArray(v) && d > 0) {
      for (let i = v.length - 1; i >= 0; i--) a.push([v[i], d - 1]);
    } else {
      b.push(v);
    }
  }
  return b;
};
```

## Group By

https://leetcode.com/problems/group-by/description/

```js
/**
 * @param {Function} fn
 * @return {Object}
 */
Array.prototype.groupBy = function (fn) {
  let a = {};
  for (let val of this) {
    const b = fn(val);
    a[b] = a[b] || [];
    a[b].push(val);
  }
  return a;
};

/**
 * [1,2,3].groupBy(String) // {"1":[1],"2":[2],"3":[3]}
 */
```

## Check if Object Instance of Class

https://leetcode.com/problems/check-if-object-instance-of-class/description/

```js
/**
 * @param {*} obj
 * @param {*} classFunction
 * @return {boolean}
 */
const checkIfInstanceOf = (obj, fn) => {
  if (obj == null || typeof fn !== 'function') return false;
  for (let p = Object.getPrototypeOf(Object(obj)); p; p = Object.getPrototypeOf(p)) if (p === fn.prototype) return true;
  return false;
};

/**
 * checkIfInstanceOf(new Date(), Date); // true
 */
```

## Call Function with Custom Context

https://leetcode.com/problems/call-function-with-custom-context/description/

```js
/**
 * @param {Object} context
 * @param {Array} args
 * @return {null|boolean|number|string|Array|Object}
 */
Function.prototype.callPolyfill = function (context, ...args) {
  const fn = this.bind(context);
  return fn(...args);
};

/**
 * function increment() { this.count++; return this.count; }
 * increment.callPolyfill({count: 1}); // 2
 */
```

## Event Emitter

https://leetcode.com/problems/event-emitter/description/

```js
class EventEmitter {
  constructor() {
    this.map = new Map();
  }
  /**
   * @param {string} eventName
   * @param {Function} callback
   * @return {Object}
   */
  subscribe(eventName, callback) {
    if (!this.map.has(eventName)) this.map.set(eventName, new Set());
    const set = this.map.get(eventName);
    set.add(callback);

    return {
      unsubscribe: () => set.delete(callback),
    };
  }

  /**
   * @param {string} eventName
   * @param {Array} args
   * @return {Array}
   */
  emit(eventName, args = []) {
    return [...(this.map.get(eventName) || [])].map((fn) => fn(...args));
  }
}

/**
 * const emitter = new EventEmitter();
 *
 * // Subscribe to the onClick event with onClickCallback
 * function onClickCallback() { return 99 }
 * const sub = emitter.subscribe('onClick', onClickCallback);
 *
 * emitter.emit('onClick'); // [99]
 * sub.unsubscribe(); // undefined
 * emitter.emit('onClick'); // []
 */
```

## Nested Array Generator

https://leetcode.com/problems/nested-array-generator/description/

```js
/**
 * @param {Array} arr
 * @return {Generator}
 */
/**
 * @param {Array} arr
 * @return {Generator<number>}
 */
const inorderTraversal = function* (arr) {
  for (const x of arr) {
    if (Array.isArray(x)) {
      yield* inorderTraversal(x);
    } else {
      yield x;
    }
  }
};

/**
 * const gen = inorderTraversal([1, [2, 3]]);
 * gen.next().value; // 1
 * gen.next().value; // 2
 * gen.next().value; // 3
 */
```

---

---

---

# Array & Hashing

## Append Characters to String to Make Subsequence

https://neetcode.io/problems/append-characters-to-string-to-make-subsequence/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {string} t
   * @return {number}
   */
  appendCharacters(s, t) {
    let i1 = 0,
      i2 = 0;
    while (i1 < s.length && i2 < t.length) {
      i2 = s[i1] == t[i2] ? i2 + 1 : i2;
      i1++;
    }
    return t.length - i2;
  }
}
```

## Group Anagrams

https://neetcode.io/problems/anagram-groups/question

```js
class Solution {
  /**
   * @param {string[]} strs
   * @return {string[][]}
   */
  groupAnagrams(strs) {
    let a = {};
    for (let s of strs) {
      const b = [...s].sort().join('');
      a[b] ??= [];
      a[b].push(s);
    }
    return Object.values(a);
  }
}
```

## Count Vowel Strings in Ranges

https://leetcode.com/problems/count-vowel-strings-in-ranges/description/

```js
/**
 * @param {string[]} words
 * @param {number[][]} queries
 * @return {number[]}
 */
const vowelStrings = (words, queries) => {
  const re = /[aeiou]/;
  let a = [0];
  for (let i of words) {
    const c = re.test(i[0]) && re.test(i.at(-1)) ? 1 : 0;
    a.push(a.at(-1) + c);
  }
  let b = [];
  for (let [l, r] of queries) b.push(a[r + 1] - a[l]);
  return b;
};
```

```js
/**
 * @param {string[]} words
 * @param {number[][]} queries
 * @return {number[]}
 */
const vowelStrings = (words, queries) => {
  const re = /[aeiou]/;
  let a = [0];
  for (let i of words) {
    const c = re.test(i[0]) && re.test(i.at(-1)) ? 1 : 0;
    a.push(a.at(-1) + c);
  }
  return queries.map(([l, r]) => a[r + 1] - a[l]);
};
```

## Average Waiting Time

https://leetcode.com/problems/average-waiting-time/description/

```js
/**
 * @param {number[][]} customers
 * @return {number}
 */
const averageWaitingTime = (customers) => {
  let b = 0,
    c = 0;
  for (let [a, t] of customers) {
    c = c < a ? a + t : c + t;
    b += c - a;
  }
  return b / customers.length;
};
```

## Sort an Array

https://neetcode.io/problems/sort-an-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  sortArray(nums) {
    let a = true;
    while (a) {
      a = false;
      for (let i = 1; i < nums.length; i++) {
        if (nums[i] < nums[i - 1]) [nums[i - 1], nums[i], a] = [nums[i], nums[i - 1], true];
      }
    }
    return nums;
  }
}
```

## Sort Colors

https://neetcode.io/problems/sort-colors/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {void} Do not return anything, modify nums in-place instead.
   */
  sortColors(nums) {
    let i = 0,
      i1 = 0,
      i2 = nums.length - 1;
    while (i <= i2) {
      if (nums[i] == 0) {
        [nums[i1], nums[i]] = [nums[i], nums[i1]];
        i1++;
        i++;
      } else if (nums[i] == 2) {
        [nums[i2], nums[i]] = [nums[i], nums[i2]];
        i2--;
      } else i++;
    }
    return nums;
  }
}
```

## Custom Sort String

https://neetcode.io/problems/custom-sort-string/question

```js
class Solution {
  /**
   * @param {string} order
   * @param {string} s
   * @return {string}
   */
  customSortString(order, s) {
    let a = {};
    for (let i of s) a[i] = (a[i] ?? '') + i;
    let b = '';
    for (let i of order) if (a[i]) [b, a[i]] = [b + a[i], ''];
    for (let i in a) b += a[i];
    return b;
  }
}
```

```js
class Solution {
  /**
   * @param {string} order
   * @param {string} s
   * @return {string}
   */
  customSortString(order, s) {
    const a = {};
    for (let i of s) a[i] = (a[i] ?? 0) + 1;
    let b = '';
    for (let i of order) {
      while (a[i] > 0) {
        b += i;
        a[i]--;
      }
    }
    for (let i in a) {
      while (a[i] > 0) {
        b += i;
        a[i]--;
      }
    }
    return b;
  }
}
```

## Top K Frequent Elements

https://neetcode.io/problems/top-k-elements-in-list/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number[]}
   */
  topKFrequent(nums, k) {
    let a = {};
    for (let i of nums) a[i] = (a[i] ?? 0) + 1;
    return Object.entries(a)
      .sort((x1, x2) => x2[1] - x1[1])
      .slice(0, k)
      .map((x) => +x[0]);
  }
}
```

## Encode and Decode Strings

https://neetcode.io/problems/string-encode-and-decode/question

```js
class Solution {
  /**
   * @param {string[]} strs
   * @returns {string}
   */
  encode(strs) {
    let a = '';
    for (let i of strs) a += i.length + '!' + i;
    return a;
  }

  /**
   * @param {string} str
   * @returns {string[]}
   */
  decode(str) {
    let a = [];
    while (str.length > 0) {
      const b = str.indexOf('!');
      const c = +str.slice(0, b);
      str = str.slice(b + 1);
      a.push(str.slice(0, c));
      str = str.slice(c);
    }
    return a;
  }
}
```

## Range Sum Query 2D Immutable

https://neetcode.io/problems/range-sum-query-2d-immutable/question

```js
class NumMatrix {
  /**
   * @param {number[][]} matrix
   */
  constructor(matrix) {
    this.matrix = matrix;
  }

  /**
   * @param {number} row1
   * @param {number} col1
   * @param {number} row2
   * @param {number} col2
   * @return {number}
   */
  sumRegion(row1, col1, row2, col2) {
    let a = 0;
    for (let i = row1; i <= row2; i++) {
      for (let j = col1; j <= col2; j++) a += this.matrix[i][j];
    }
    return a;
  }
}

/**
 * Your NumMatrix object will be instantiated and called as such:
 * var obj = new NumMatrix(matrix)
 * var param_1 = obj.sumRegion(row1,col1,row2,col2)
 */
```

## Analyze User Website Visit Pattern

https://neetcode.io/problems/analyze-user-website-visit-pattern/question

```js
class Solution {
  /**
   * @param {string[]} username
   * @param {number[]} timestamp
   * @param {string[]} website
   * @return {string[]}
   */
  mostVisitedPattern(username, timestamp, website) {
    const n = username.length;
    let arr = [];
    for (let i = 0; i < n; i++) arr.push([timestamp[i], username[i], website[i]]);
    arr.sort((x1, x2) => {
      if (x1[1] == x2[1]) return x1[0] - x2[0];
      return x1[1] < x2[1] ? -1 : 1;
    });

    let a = {},
      i = 0;
    while (i < n) {
      let j = i;
      let b = [];
      while (j < n && arr[j][1] === arr[i][1]) {
        b.push(arr[j][2]);
        j++;
      }

      let c = new Set();
      let d = b.length;

      for (let x = 0; x < d; x++) {
        for (let y = x + 1; y < d; y++) {
          for (let z = y + 1; z < d; z++) {
            const k = b[x] + '!' + b[y] + '!' + b[z];
            if (!c.has(k)) {
              c.add(k);
              a[k] = (a[k] || 0) + 1;
            }
          }
        }
      }
      i = j;
    }
    let e = null,
      f = 0;
    for (let k in a) {
      if (a[k] > f || (a[k] == f && k < e)) {
        e = k;
        f = a[k];
      }
    }
    return e.split('!');
  }
}
```

## Products of Array Except Self

https://neetcode.io/problems/products-of-array-discluding-self/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  productExceptSelf(nums) {
    const n = nums.length;
    let a = [];
    let b = 1;
    for (let i = 0; i < n; i++) [a[i], b] = [b, b * nums[i]];
    b = 1;
    for (let i = n - 1; i >= 0; i--) [a[i], b] = [a[i] * b, b * nums[i]];
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  productExceptSelf(nums) {
    const n = nums.length;
    let a = 1,
      b = false,
      c;
    for (let i = 0; i < n; i++) {
      if (nums[i] == 0) {
        if (b) return Array(n).fill(0);
        b = true;
        c = i;
        continue;
      }
      a *= nums[i];
    }
    if (b) {
      let d = Array(n).fill(0);
      d[c] = a;
      return d;
    }
    return nums.map((x) => a / x);
  }
}
```

## Minimum Number of Operations to Move All Balls to Each Box

https://leetcode.com/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/description/

```js
/**
 * @param {string} boxes
 * @return {number[]}
 */
const minOperations = (boxes) => {
  const n = boxes.length;
  let a = [];
  for (let i = 0; i < n; i++) {
    let b = 0;
    for (let j = 0; j < n; j++) {
      if (boxes[j] == '0') continue;
      b += Math.abs(i - j);
    }
    a.push(b);
  }
  return a;
};
```

```js
/**
 * @param {string} boxes
 * @return {number[]}
 */
const minOperations = (boxes) => {
  const n = boxes.length;
  let a = Array(n).fill(0);
  let b = 0,
    c = 0;
  for (let i = 0; i < n; i++) {
    a[i] += c;
    b += boxes[i] == '1';
    c += b;
  }
  ((b = 0), (c = 0));
  for (let i = n - 1; i >= 0; i--) {
    a[i] += c;
    b += boxes[i] == '1';
    c += b;
  }
  return a;
};
```

## Valid Sudoku

https://neetcode.io/problems/valid-sudoku/question

```js
class Solution {
  /**
   * @param {character[][]} board
   * @return {boolean}
   */
  isValidSudoku(board) {
    const row = Array.from({ length: 9 }, () => []);
    const col = Array.from({ length: 9 }, () => []);
    const box = Array.from({ length: 9 }, () => []);

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const v = board[r][c];
        if (v == '.') continue;
        const b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
        if (row[r].includes(v) || col[c].includes(v) || box[b].includes(v)) return false;

        row[r].push(v);
        col[c].push(v);
        box[b].push(v);
      }
    }
    return true;
  }
}
```

```js
class Solution {
  /**
   * @param {character[][]} board
   * @return {boolean}
   */
  isValidSudoku(board) {
    const row = Array.from({ length: 9 }, () => []);
    const col = Array.from({ length: 9 }, () => []);
    const box = Array.from({ length: 9 }, () => []);

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const v = board[r][c];
        if (v == '.') continue;
        const b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
        if (row[r].includes(v) || col[c].includes(v) || box[b].includes(v)) return false;

        row[r].push(v);
        col[c].push(v);
        box[b].push(v);
      }
    }
    return true;
  }
}
```

```js
class Solution {
  /**
   * @param {character[][]} board
   * @return {boolean}
   */
  isValidSudoku(board) {
    const row = Array.from({ length: 9 }, () => Array(10).fill(false));
    const col = Array.from({ length: 9 }, () => Array(10).fill(false));
    const box = Array.from({ length: 9 }, () => Array(10).fill(false));

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const v = board[r][c];
        if (v == '.') continue;
        const i = +v;
        const b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
        if (row[r][i] || col[c][i] || box[b][i]) return false;

        row[r][i] = true;
        col[c][i] = true;
        box[b][i] = true;
      }
    }
    return true;
  }
}
```

```js
class Solution {
  /**
   * @param {character[][]} board
   * @return {boolean}
   */
  isValidSudoku(board) {
    const row = Array(9).fill(0);
    const col = Array(9).fill(0);
    const box = Array(9).fill(0);

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const v = board[r][c];
        if (v == '.') continue;
        const i = +v;
        const bit = 1 << i;
        const b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
        if (row[r] & bit || col[c] & bit || box[b] & bit) return false;

        row[r] |= bit;
        col[c] |= bit;
        box[b] |= bit;
      }
    }
    return true;
  }
}
```

## Longest Consecutive Sequence

https://neetcode.io/problems/longest-consecutive-sequence/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  longestConsecutive(nums) {
    let a = [...new Set(nums)].sort((x1, x2) => x1 - x2);
    console.log(a);
    let b = 0,
      l = 0;
    for (let r = 1; r < a.length; r++) {
      if (a[r] - a[r - 1] == 1) continue;
      b = r - l > b ? r - l : b;
      l = r;
    }
    b = Math.max(b, a.length - l);
    return b;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  longestConsecutive(nums) {
    const a = new Set(nums);
    let b = 0;
    for (let i of a) {
      if (!a.has(i - 1)) {
        let c = i,
          d = 1;
        while (a.has(c + 1)) [c, d] = [c + 1, d + 1];
        b = d > b ? d : b;
      }
    }
    return b;
  }
}
```

## Encode and Decode TinyURL

https://leetcode.com/problems/encode-and-decode-tinyurl/description/

```js
const ids = new Map();
let id = 0;

/**
 * Encodes a URL to a shortened URL.
 *
 * @param {string} longUrl
 * @return {string}
 */

const encode = (longUrl) => {
  id++;
  ids.set(id.toString(), longUrl);
  return 'http://tinyurl.com/' + id;
};

/**
 * Decodes a shortened URL to its original URL.
 *
 * @param {string} shortUrl
 * @return {string}
 */
const decode = (shortUrl) => {
  const id = shortUrl.split('/').pop();
  return ids.get(id);
};

/**
 * Your functions will be called as such:
 * decode(encode(url));
 */
```

## Brick Wall

https://leetcode.com/problems/brick-wall/description/

```js
/**
 * @param {number[][]} wall
 * @return {number}
 */
const leastBricks = (wall) => {
  let a = [];
  for (let arr of wall) {
    let b = 0;
    for (let i of arr.slice(0, -1)) {
      b += i;
      a.push(b);
    }
  }
  let c = {},
    d = 0;
  for (let i of a) {
    c[i] = (c[i] ?? 0) + 1;
    d = c[i] > d ? c[i] : d;
  }
  return wall.length - d;
};
```

```js
/**
 * @param {number[][]} wall
 * @return {number}
 */
const leastBricks = (wall) => {
  let a = {},
    b = 0;
  for (let arr of wall) {
    let c = 0;
    for (let i = 0; i < arr.length - 1; i++) {
      c += arr[i];
      a[c] = (a[c] ?? 0) + 1;
      b = a[c] > b ? a[c] : b;
    }
  }
  return wall.length - b;
};
```

## Best Time to Buy and Sell Stock II

https://neetcode.io/problems/best-time-to-buy-and-sell-stock-ii/question

```js
class Solution {
  /**
   * @param {number[]} prices
   * @return {number}
   */
  maxProfit(prices) {
    let a = 0;
    for (let i = 1; i < prices.length; i++) {
      a += prices[i] > prices[i - 1] ? prices[i] - prices[i - 1] : 0;
    }
    return a;
  }
}
```

## Majority Element II

https://neetcode.io/problems/majority-element-ii/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  majorityElement(nums) {
    let a1,
      a2,
      b1 = 0,
      b2 = 0;
    for (let i of nums) {
      if (i == a1) b1++;
      else if (i == a2) b2++;
      else if (b1 == 0) [a1, b1] = [i, 1];
      else if (b2 == 0) [a2, b2] = [i, 1];
      else [b1, b2] = [b1 - 1, b2 - 1];
    }
    ((b1 = 0), (b2 = 0));
    for (let i of nums) {
      if (i == a1) b1++;
      else if (i == a2) b2++;
    }
    let c = [];
    if (b1 > nums.length / 3) c.push(a1);
    if (b2 > nums.length / 3) c.push(a2);
    return c;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  majorityElement(nums) {
    let a = [];
    for (let i of nums) a[i] = (a[i] ?? 0) + 1;
    let b = [];
    for (let i in a) {
      if (a[i] > nums.length / 3) b.push(i);
    }
    return b;
  }
}
```

## Minimum Index of a Valid Split

https://leetcode.com/problems/minimum-index-of-a-valid-split/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const minimumIndex = (nums) => {
  let a,
    b = 0;
  for (let i of nums) {
    if (i == a) b++;
    else if (b == 0) [a, b] = [i, 1];
    else b--;
  }
  b = 0;
  for (let i of nums) b += i == a ? 1 : 0;
  let c = 0;
  for (let i = 0; i < nums.length - 1; i++) {
    if (nums[i] == a) c++;
    if (c * 2 > i + 1 && (b - c) * 2 > nums.length - i - 1) return i;
  }
  return -1;
};
```

## Subarray Sum Equals K

https://neetcode.io/problems/subarray-sum-equals-k/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  subarraySum(nums, k) {
    let a = 0;
    for (let l = 0; l < nums.length; l++) {
      let b = 0;
      for (let r = l; r < nums.length; r++) {
        b += nums[r];
        if (b == k) a++;
      }
    }
    return a;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  subarraySum(nums, k) {
    let a = { 0: 1 },
      b = 0,
      c = 0;
    for (let i of nums) {
      b += i;
      c += a[b - k] ?? 0;
      a[b] = (a[b] ?? 0) + 1;
    }
    return c;
  }
}
```

## Subarray Sums Divisible by K

https://leetcode.com/problems/subarray-sums-divisible-by-k/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const subarraysDivByK = (nums, k) => {
  let a = { 0: 1 },
    b = 0,
    c = 0;
  for (let i of nums) {
    b += i;
    const d = ((b % k) + k) % k;
    c += a[d] ?? 0;
    a[d] = (a[d] ?? 0) + 1;
  }
  return c;
};
```

## Make Sum Divisible by P

https://leetcode.com/problems/make-sum-divisible-by-p/description/

```js
/**
 * @param {number[]} nums
 * @param {number} p
 * @return {number}
 */
const minSubarray = (nums, p) => {
  const n = nums.length;
  const e = nums.reduce((a, x) => a + x, 0) % p;
  if (e == 0) return 0;
  let a = { 0: -1 },
    b = 0,
    c = n;
  for (let i = 0; i < n; i++) {
    b = (b + nums[i]) % p;
    const d = (b - e + p) % p;
    if (d in a) c = i - a[d] < c ? i - a[d] : c;
    a[b] = i;
  }
  return c == n ? -1 : c;
};
```

## Unique Length-3 Palindromic Subsequences

https://leetcode.com/problems/unique-length-3-palindromic-subsequences/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const countPalindromicSubsequence = (s) => {
  let a = {};
  for (let i = 0; i < s.length; i++) {
    if (!a[s[i]]) a[s[i]] = [];
    a[s[i]].push(i);
  }
  let b = 0;
  for (let k in a) {
    let arr = a[k];
    if (arr.length < 2) continue;
    let l = arr[0];
    let r = arr.at(-1);
    b += new Set(s.slice(l + 1, r)).size;
  }
  return b;
};
```

```js
/**
 * @param {string} s
 * @return {number}
 */
const countPalindromicSubsequence = (s) => {
  const n = s.length;
  let l = new Array(26).fill(0);
  let r = new Array(26).fill(0);
  let a = Array.from({ length: 26 }, () => new Array(26).fill(0));

  for (let c of s) r[c.charCodeAt(0) - 97]++;
  let b = 0;
  for (let i = 0; i < n; i++) {
    let m = s.charCodeAt(i) - 97;
    r[m]--;
    for (let x = 0; x < 26; x++) {
      if (l[x] && r[x] && !a[x][m]) [a[x][m], b] = [1, b + 1];
    }
    l[m]++;
  }
  return b;
};
```

## Number of Sub-arrays With Odd Sum

https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/description/

```js
/**
 * @param {number[]} arr
 * @return {number}
 */
const numOfSubarrays = (arr) => {
  let a = 0,
    b = 0,
    c = 1,
    d = 0;
  for (let i of arr) {
    b += i;
    if (b % 2 == 0) [a, c] = [a + d, c + 1];
    else [a, d] = [a + c, d + 1];
    a %= 1e9 + 7;
  }
  return a;
};
```

## Minimum Number of Swaps to Make the String Balanced

https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const minSwaps = (s) => {
  let a = 0,
    b = 0;
  for (let i of s) {
    if (i == '[') a++;
    else {
      if (a > 0) a--;
      else [a, b] = [a + 1, b + 1];
    }
  }
  return b;
};
```

## Number of Pairs of Interchangeable Rectangles

https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/description/

```js
/**
 * @param {number[][]} rectangles
 * @return {number}
 */
const interchangeableRectangles = (rectangles) => {
  let a = [];
  for (let [w, h] of rectangles) a[w / h] = (a[w / h] ?? 0) + 1;
  let b = 0;
  for (let i in a) {
    if (a[i] == 1) continue;
    b += (a[i] * (a[i] - 1)) / 2;
  }
  return b;
};
```

```js
/**
 * @param {number[][]} rectangles
 * @return {number}
 */
const interchangeableRectangles = (rectangles) => {
  const a = {};
  let b = 0;
  for (let [w, h] of rectangles) {
    const c = a[w / h] ?? 0;
    [b, a[w / h]] = [b + c, c + 1];
  }
  return b;
};
```

## Maximum Product of the Length of Two Palindromic Subsequences

https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const maxProduct = (s) => {
  let c = 0;
  const isPal = (str) => {
    let l = 0,
      r = str.length - 1;
    while (l < r) if (str[l++] !== str[r--]) return false;
    return true;
  };
  const dfs = (i, a, b) => {
    if (i === s.length) {
      if (isPal(a) && isPal(b)) c = Math.max(c, a.length * b.length);
      return;
    }
    dfs(i + 1, a + s[i], b);
    dfs(i + 1, a, b + s[i]);
    dfs(i + 1, a, b);
  };

  dfs(0, '', '');
  return c;
};
```

## Grid Game

https://leetcode.com/problems/grid-game/description/

```js
/**
 * @param {number[][]} grid
 * @return {number}
 */
const gridGame = (grid) => {
  const n = grid[0].length;
  let a = grid[0].reduce((a, x) => a + x, 0),
    b = 0,
    c = Infinity;
  for (let i = 0; i < n; i++) {
    a -= grid[0][i];
    c = Math.min(c, Math.max(a, b));
    b += grid[1][i];
  }
  return c;
};
```

## Find All Anaglams in a String

https://leetcode.com/problems/find-all-anagrams-in-a-string/description/

```js
/**
 * @param {string} s
 * @param {string} p
 * @return {number[]}
 */
const findAnagrams = (s, p) => {
  const a = [];
  const b = Array(26).fill(0);
  const c = Array(26).fill(0);

  for (let i of p) b[i.charCodeAt(0) - 97]++;
  let l = 0;
  for (let r = 0; r < s.length; r++) {
    c[s[r].charCodeAt(0) - 97]++;
    if (r - l + 1 > p.length) {
      c[s[l].charCodeAt(0) - 97]--;
      l++;
    }
    if (r - l + 1 == p.length) {
      let d = true;
      for (let i = 0; i < 26; i++) {
        if (c[i] != b[i]) {
          d = false;
          break;
        }
      }
      if (d) a.push(l);
    }
  }
  return a;
};
```

## Wiggle Sort

https://neetcode.io/problems/wiggle-sort/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {void} Do not return anything, modify nums in-place instead.
   */
  wiggleSort(nums) {
    nums.sort((x1, x2) => x1 - x2);
    for (let i = 1; i < nums.length - 1; i += 2) {
      [nums[i], nums[i + 1]] = [nums[i + 1], nums[i]];
    }
    return nums;
  }
}
```

## Largest Number

https://neetcode.io/problems/largest-number/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {string}
   */
  largestNumber(nums) {
    return (
      nums
        .map(String)
        .sort((x1, x2) => (x2 + x1 > x1 + x2 ? 1 : x2 + x1 < x1 + x2 ? -1 : 0))
        .join('')
        .replace(/^0+/, '') || '0'
    );
  }
}
```

## Continuous Subarray Sum

https://neetcode.io/problems/continuous-subarray-sum/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {boolean}
   */
  checkSubarraySum(nums, k) {
    for (let i = 0; i < nums.length - 1; i++) {
      let a = nums[i];
      for (let j = i + 1; j < nums.length; j++) {
        a += nums[j];
        if (a % k == 0) return true;
      }
    }
    return false;
  }
}
```

## Push Dominoes

https://leetcode.com/problems/push-dominoes/description/

```js
/**
 * @param {string} dominoes
 * @return {string}
 */
const pushDominoes = (dominoes) => {
  let a = [...('L' + dominoes + 'R')],
    i1 = 0;
  for (let i = 1; i < a.length; i++) {
    if (a[i] == '.') continue;
    else if (a[i] == 'R') {
      if (a[i1] == 'R') while (i1 < i) a[i1++] = 'R';
    } else if (a[i1] == 'L') while (i1 < i) a[i1++] = 'L';
    else {
      let i2 = i;
      while (i1 < i2) [a[i1++], a[i2--]] = ['R', 'L'];
    }
    i1 = i;
  }
  return a.slice(1, -1).join('');
};
```

```js
/**
 * @param {string} dominoes
 * @return {string}
 */
const pushDominoes = (dominoes) => {
  let a = [...('L' + dominoes + 'R')];
  let i = 0;
  for (let j = 1; j < a.length; j++) {
    if (a[j] == '.') continue;
    if (j - i > 1) {
      if (a[i] == a[j]) {
        for (let k = i + 1; k < j; k++) a[k] = a[i];
      } else if (a[i] == 'R' && a[j] == 'L') {
        let l = i + 1,
          r = j - 1;
        while (l < r) [a[l++], a[r--]] = ['R', 'L'];
      }
    }
    i = j;
  }
  return a.slice(1, -1).join('');
};
```

## Repeated DNA Sequences

https://leetcode.com/problems/repeated-dna-sequences/description/

```js
/**
 * @param {string} s
 * @return {string[]}
 */
const findRepeatedDnaSequences = (s) => {
  let a = {},
    b = new Set();
  for (let i = 0; i <= s.length - 10; i++) {
    const c = s.slice(i, i + 10);
    if (a[c]) b.add(c);
    else a[c] = true;
  }
  return [...b];
};
```

## Insert Delete Get Random O(1)

https://neetcode.io/problems/insert-delete-getrandom-o1/question

```js
class RandomizedSet {
  constructor() {
    this.vals = new Set();
  }

  /**
   * @param {number} val
   * @return {boolean}
   */
  insert(val) {
    const a = this.vals.has(val);
    this.vals.add(val);
    return a;
  }

  /**
   * @param {number} val
   * @return {boolean}
   */
  remove(val) {
    const a = this.vals.has(val);
    this.vals.delete(val);
  }

  /**
   * @return {number}
   */
  getRandom() {
    const a = [...this.vals];
    return a[(Math.random() * a.length) | 0];
  }
}

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * var obj = new RandomizedSet()
 * var param_1 = obj.insert(val)
 * var param_2 = obj.remove(val)
 * var param_3 = obj.getRandom()
 */
```

## Check if a String Contains All binary Codes of Size K

https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/description/

```js
/**
 * @param {string} s
 * @param {number} k
 * @return {boolean}
 */
const hasAllCodes = (s, k) => {
  let a = Array(2 ** k).fill(false);
  for (let i = 0; i <= s.length - k; i++) a[parseInt(s.slice(i, i + k), 2)] = true;
  return !a.includes(false);
};
```

## Non Decreasing Array

https://leetcode.com/problems/non-decreasing-array/description/

```js
/**
 * @param {number[]} nums
 * @return {boolean}
 */
const checkPossibility = (nums) => {
  let a = false;
  for (let i = 1; i < nums.length; i++) {
    if (nums[i - 1] > nums[i]) {
      if (a) return false;
      a = true;
      if (i < 2 || nums[i - 2] <= nums[i]) nums[i - 1] = nums[i];
      else nums[i] = nums[i - 1];
    }
  }
  return true;
};
```

```js
/**
 * @param {number[]} nums
 * @return {boolean}
 */
const checkPossibility = (nums) => {
  let a1 = -Infinity,
    a2 = nums[0];
  let b = false;
  for (let i of nums.slice(1)) {
    if (i < a2) {
      if (b) return false;
      b = true;
      if (i >= a1) a2 = i;
    } else [a1, a2] = [a2, i];
  }
  return true;
};
```

## Number of Ways to Split Array

https://leetcode.com/problems/number-of-ways-to-split-array/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const waysToSplitArray = (nums) => {
  const a = nums.reduce((a, x) => a + x, 0);
  let b = 0,
    c = 0;
  for (let i of nums.slice(0, -1)) {
    b += i;
    if (b >= a - b) c++;
  }
  return c;
};
```

## Shifting Letters II

https://leetcode.com/problems/shifting-letters-ii/description/

```js
/**
 * @param {string} s
 * @param {number[][]} shifts
 * @return {string}
 */
const shiftingLetters = (s, shifts) => {
  let a = [];
  for (let i = 0; i < s.length; i++) a.push(s.charCodeAt(i) - 97);
  for (let [l, r, d] of shifts) {
    for (let i = l; i <= r; i++) {
      a[i] += d * 2 - 1;
      a[i] += a[i] < 0 ? 26 : 0;
    }
  }
  for (let i = 0; i < a.length; i++) a[i] = String.fromCharCode((a[i] % 26) + 97);
  return a.join('');
};
```

```js
/**
 * @param {string} s
 * @param {number[][]} shifts
 * @return {string}
 */
const shiftingLetters = (s, shifts) => {
  let a = Array(s.length + 1).fill(0);
  for (let [l, r, d] of shifts) {
    const b = d ? 1 : -1;
    ((a[l] += b), (a[r + 1] -= b));
  }
  let b = 0,
    c = [];
  for (let i = 0; i < s.length; i++) {
    b += a[i];
    let d = s.charCodeAt(i) - 97;
    d = (d + b) % 26;
    d += d < 0 ? 26 : 0;
    c.push(String.fromCharCode(d + 97));
  }
  return c.join('');
};
```

## Number of Zero Filled Subarrays

https://leetcode.com/problems/number-of-zero-filled-subarrays/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const zeroFilledSubarray = (nums) => {
  let a = 0,
    b = 0;
  for (let i of nums) {
    b = i == 0 ? b + 1 : 0;
    a += b;
  }
  return a;
};
```

## Word Subsets

https://leetcode.com/problems/word-subsets/description/

```js
/**
 * @param {string[]} words1
 * @param {string[]} words2
 * @return {string[]}
 */
const wordSubsets = (words1, words2) => {
  let a = [],
    b = [];
  for (let i = 0; i < words2.length; i++) {
    b[i] = {};
    for (let c of words2[i]) b[i][c] = (b[i][c] ?? 0) + 1;
  }
  for (let s of words1) {
    let e = false;
    let d = {};
    for (let c of s) d[c] = (d[c] ?? 0) + 1;
    for (let o of b) {
      for (let i in o) {
        if ((d[i] ?? 0) < o[i]) {
          e = true;
          break;
        }
      }
      if (e) break;
    }
    if (!e) a.push(s);
  }
  return a;
};
```

```js
/**
 * @param {string[]} words1
 * @param {string[]} words2
 * @return {string[]}
 */
const wordSubsets = (words1, words2) => {
  let a = [],
    b = {};
  for (let s of words2) {
    let c = {};
    for (let i of s) c[i] = (c[i] ?? 0) + 1;
    for (let i in c) b[i] = Math.max(b[i] ?? 0, c[i]);
  }
  for (let s of words1) {
    let e = true;
    let c = {};
    for (let i of s) c[i] = (c[i] ?? 0) + 1;
    for (let i in b) {
      if ((c[i] ?? 0) < b[i]) {
        e = false;
        break;
      }
    }
    if (e) a.push(s);
  }
  return a;
};
```

```js
/**
 * @param {string[]} words1
 * @param {string[]} words2
 * @return {string[]}
 */
const wordSubsets = (words1, words2) => {
  let a = [];
  let b = Array(26).fill(0);
  for (let s of words2) {
    let c = Array(26).fill(0);
    for (let i of s) c[i.charCodeAt(0) - 97]++;
    for (let i = 0; i < 26; i++) b[i] = Math.max(b[i], c[i]);
  }

  for (let s of words1) {
    let c = Array(26).fill(0);
    for (let i of s) c[i.charCodeAt(0) - 97]++;

    let e = true;
    for (let i = 0; i < 26; i++) {
      if (c[i] < b[i]) {
        e = false;
        break;
      }
    }
    if (e) a.push(s);
  }
  return a;
};
```

## Optimal Partition of String

https://leetcode.com/problems/optimal-partition-of-string/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const partitionString = (s) => {
  let a = 1,
    c = {};
  for (let i = 0; i < s.length; i++) {
    if (c[s[i]]) [a, c] = [a + 1, {}];
    c[s[i]] = true;
  }
  return a;
};
```

```js
/**
 * @param {string} s
 * @return {number}
 */
const partitionString = (s) => {
  let a = 1;
  let b = Array(26).fill(0);
  for (const c of s) {
    const i = c.charCodeAt(0) - 97;
    if (b[i] == a) a++;
    b[i] = a;
  }
  return a;
};
```

## Design Underground System

https://leetcode.com/problems/design-underground-system/description/

```js
const UndergroundSystem = function () {
  this.checkin = new Map();
  this.routes = new Map();
};

/**
 * @param {number} id
 * @param {string} stationName
 * @param {number} t
 * @return {void}
 */
UndergroundSystem.prototype.checkIn = function (id, stationName, t) {
  this.checkin.set(id, [stationName, t]);
};

/**
 * @param {number} id
 * @param {string} stationName
 * @param {number} t
 * @return {void}
 */
UndergroundSystem.prototype.checkOut = function (id, stationName, t) {
  const [startStation, startTime] = this.checkin.get(id);

  const key = startStation + '-' + stationName;

  const time = t - startTime;

  if (!this.routes.has(key)) {
    this.routes.set(key, [0, 0]);
  }

  const [total, count] = this.routes.get(key);

  this.routes.set(key, [total + time, count + 1]);

  this.checkin.delete(id);
};

/**
 * @param {string} startStation
 * @param {string} endStation
 * @return {number}
 */
UndergroundSystem.prototype.getAverageTime = function (startStation, endStation) {
  const [total, count] = this.routes.get(startStation + '-' + endStation);

  return total / count;
};

/**
 * Your UndergroundSystem object will be instantiated and called as such:
 * var obj = new UndergroundSystem()
 * obj.checkIn(id,stationName,t)
 * obj.checkOut(id,stationName,t)
 * var param_3 = obj.getAverageTime(startStation,endStation)
 */
```

## Minimum Penalty for a Shop

https://leetcode.com/problems/minimum-penalty-for-a-shop/description/

```js
/**
 * @param {string} customers
 * @return {number}
 */
const bestClosingTime = (customers) => {
  let a = -1,
    b = 0,
    c = 0;
  for (let i = 0; i < customers.length; i++) {
    c = customers[i] == 'Y' ? c - 1 : c + 1;
    [a, b] = c < b ? [i, c] : [a, b];
  }
  return a + 1;
};
```

## Champagne Tower

https://leetcode.com/problems/champagne-tower/description/

```js
/**
 * @param {number} poured
 * @param {number} query_row
 * @param {number} query_glass
 * @return {number}
 */
const champagneTower = (poured, query_row, query_glass) => {
  let dp = [];
  for (let i = 0; i <= query_row + 1; i++) dp[i] = Array(i + 1).fill(0);
  dp[0][0] = poured;
  for (let i = 0; i <= query_row; i++) {
    for (let j = 0; j <= i; j++) {
      const a = dp[i][j] - 1;
      if (a > 0) {
        dp[i + 1][j] += a / 2;
        dp[i + 1][j + 1] += a / 2;
      }
    }
  }
  return Math.min(1, dp[query_row][query_glass]);
};
```

## Sum of Absolute Differences in a Sorted Array

https://leetcode.com/problems/sum-of-absolute-differences-in-a-sorted-array/description/

```js
/**
 * @param {number[]} nums
 * @return {number[]}
 */
const getSumAbsoluteDifferences = (nums) => {
  const n = nums.length;
  let a = [0];
  for (let i = 0; i < n; i++) a[i + 1] = a[i] + nums[i];
  let b = [];
  for (let i = 0; i < n; i++) {
    const l = nums[i] * i - a[i];
    const r = a[n] - a[i + 1] - nums[i] * (n - i - 1);
    b.push(l + r);
  }
  return b;
};
```

```js
/**
 * @param {number[]} nums
 * @return {number[]}
 */
const getSumAbsoluteDifferences = (nums) => {
  const n = nums.length;
  const ans = Array(n);
  let total = 0;
  for (let i = 0; i < n; i++) total += nums[i];

  let leftSum = 0;
  for (let i = 0; i < n; i++) {
    const x = nums[i];
    const l = x * i - leftSum;
    const r = total - leftSum - x - x * (n - i - 1);
    ans[i] = l + r;
    leftSum += x;
  }
  return ans;
};
```

## Design a Food Rating System

https://leetcode.com/problems/design-a-food-rating-system/description/

```js
/**
 * @param {string[]} foods
 * @param {string[]} cuisines
 * @param {number[]} ratings
 */
const FoodRatings = function (foods, cuisines, ratings) {
  ((this.cuisine = {}), (this.food = {}));
  for (let i = 0; i < foods.length; i++) {
    (this.cuisine[cuisines[i]] ??= []).push(foods[i]);
    this.food[foods[i]] = { rating: ratings[i], cuisine: cuisines[i] };
  }
};

/**
 * @param {string} food
 * @param {number} newRating
 * @return {void}
 */
FoodRatings.prototype.changeRating = function (food, newRating) {
  this.food[food].rating = newRating;
};

/**
 * @param {string} cuisine
 * @return {string}
 */
FoodRatings.prototype.highestRated = function (cuisine) {
  let a = '',
    b = -1;
  for (let i of this.cuisine[cuisine]) {
    const c = this.food[i].rating;
    if (c > b || (c == b && i < a)) [a, b] = [i, c];
  }
  return a;
};

/**
 * Your FoodRatings object will be instantiated and called as such:
 * var obj = new FoodRatings(foods, cuisines, ratings)
 * obj.changeRating(food,newRating)
 * var param_2 = obj.highestRated(cuisine)
 */
```

```js
class MyHeap {
  constructor(fn1) {
    this.data = [];
    this.fn1 = fn1;
  }
  push(value) {
    const a = this.data;
    a.push(value);
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.fn1(a[p], a[i])) break;
      [a[p], a[i]] = [a[i], a[p]];
      i = p;
    }
  }
  pop() {
    const a = this.data;
    if (a.length === 1) return a.pop();
    const top = a[0];
    a[0] = a.pop();
    let i = 0;
    while (true) {
      let l = i * 2 + 1;
      let r = i * 2 + 2;
      let best = i;
      if (l < a.length && !this.fn1(a[best], a[l])) {
        best = l;
      }
      if (r < a.length && !this.fn1(a[best], a[r])) {
        best = r;
      }
      if (best === i) break;
      [a[i], a[best]] = [a[best], a[i]];
      i = best;
    }
    return top;
  }
  top() {
    return this.data[0];
  }
}

/**
 * @param {string[]} foods
 * @param {string[]} cuisines
 * @param {number[]} ratings
 */
const FoodRatings = function (foods, cuisines, ratings) {
  this.food = {};
  this.heap = {};
  for (let i = 0; i < foods.length; i++) {
    const food = foods[i];
    const cuisine = cuisines[i];
    const rating = ratings[i];
    this.food[food] = {
      cuisine,
      rating,
    };
    this.heap[cuisine] ??= new MyHeap((a, b) => {
      if (a.rating !== b.rating) {
        return a.rating > b.rating;
      }
      return a.food < b.food;
    });
    this.heap[cuisine].push({
      food,
      rating,
    });
  }
};

/**
 * @param {string} food
 * @param {number} newRating
 * @return {void}
 */
FoodRatings.prototype.changeRating = function (food, newRating) {
  const cuisine = this.food[food].cuisine;
  this.food[food].rating = newRating;
  this.heap[cuisine].push({
    food,
    rating: newRating,
  });
};

/**
 * @param {string} cuisine
 * @return {string}
 */
FoodRatings.prototype.highestRated = function (cuisine) {
  const heap = this.heap[cuisine];
  while (true) {
    const top = heap.top();
    if (this.food[top.food].rating === top.rating) {
      return top.food;
    }
    heap.pop();
  }
};
```

## Convert an Array Into a 2D Array With Conditions

https://leetcode.com/problems/convert-an-array-into-a-2d-array-with-conditions/description/

```js
/**
 * @param {number[]} nums
 * @return {number[][]}
 */
const findMatrix = (nums) => {
  let a = {};
  for (let i of nums) a[i] = (a[i] ?? 0) + 1;
  let b = [],
    c = true;
  while (c) {
    c = false;
    let d = [];
    for (let i in a) {
      if (!a[i]) continue;
      a[i]--;
      d.push(+i);
      c = true;
    }
    if (c) b.push(d);
  }
  return b;
};
```

## Minimum Number of Operations to Make Array Empty

https://neetcode.io/problems/minimum-number-of-operations-to-make-array-empty/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  minOperations(nums) {
    let a = {};
    for (let i of nums) a[i] = (a[i] ?? 0) + 1;
    const b = Object.values(a);
    if (b.includes(1)) return -1;
    let c = 0;
    for (let i of b) c += i % 3 == 0 ? i / 3 : ((i / 3) | 0) + 1;
    return c;
  }
}
```

## Divide Array Into Arrays With Max Difference

https://leetcode.com/problems/divide-array-into-arrays-with-max-difference/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number[][]}
 */
const divideArray = (nums, k) => {
  nums.sort((x1, x2) => x1 - x2);
  let a = [],
    i = 0;
  for (let i = 0; i < nums.length; i += 3) {
    if (nums[i + 2] - nums[i] > k) return [];
    a.push([nums[i], nums[i + 1], nums[i + 2]]);
  }
  return a;
};
```

## Sequential Digits

https://leetcode.com/problems/sequential-digits/description/

```js
/**
 * @param {number} low
 * @param {number} high
 * @return {number[]}
 */
const sequentialDigits = (low, high) => {
  const a = [12, 123, 1234, 12345, 123456, 1234567, 12345678];
  const b = [89, 789, 6789, 56789, 456789, 3456789, 23456789];
  const c = [11, 111, 1111, 11111, 111111, 1111111, 11111111];
  let d = [];
  for (let i = 0; i < a.length; i++) {
    for (let x = a[i]; x <= b[i]; x += c[i]) {
      if (x >= low && x <= high) d.push(x);
    }
  }
  if (low <= 123456789 && high >= 123456789) d.push(123456789);
  return d;
};
```

## Sort Characters by Frequency

https://leetcode.com/problems/sort-characters-by-frequency/description/

```js
/**
 * @param {string} s
 * @return {string}
 */
const frequencySort = (s) => {
  let a = {};
  for (let i of s) a[i] = (a[i] ?? 0) + 1;
  let b = Object.entries(a);
  b.sort((x1, x2) => x2[1] - x1[1]);
  let c = '';
  for (let [k, v] of b) {
    for (let i = 0; i < v; i++) c += k;
  }
  return c;
};
```

## Sort the Jumbled Numbers

https://leetcode.com/problems/sort-the-jumbled-numbers/description/

```js
/**
 * @param {number[]} mapping
 * @param {number[]} nums
 * @return {number[]}
 */
const sortJumbled = (mapping, nums) => {
  const fn = (n) => {
    if (n == 0) return mapping[0];
    let a = '';
    while (n > 0) [a, n] = [mapping[n % 10] + a, (n / 10) | 0];
    return +a;
  };
  return nums.sort((x1, x2) => fn(x1) - fn(x2));
};
```

```js
/**
 * @param {number[]} mapping
 * @param {number[]} nums
 * @return {number[]}
 */
const sortJumbled = (mapping, nums) => {
  const fn = (n) => {
    if (n == 0) return mapping[0];
    let x = 0,
      p = 1;
    while (n) [x, p, n] = [x + mapping[n % 10] * p, p * 10, (n / 10) | 0];
    return x;
  };

  return nums
    .map((x) => [fn(x), x])
    .sort((x1, x2) => x1[0] - x2[0])
    .map((x) => x[1]);
};
```

## Find Polygon With the Largest Perimeter

https://leetcode.com/problems/find-polygon-with-the-largest-perimeter/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const largestPerimeter = (nums) => {
  nums.sort((x1, x2) => x1 - x2);
  let a = nums.reduce((a, x) => a + x, 0);
  let b = Infinity;
  while (a <= b && nums.length) {
    b = nums.pop();
    a -= b;
  }
  return a ? a + b : -1;
};
```

## Minimum Remove to make Valid Parentheses

https://neetcode.io/problems/minimum-remove-to-make-valid-parentheses/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {string}
   */
  minRemoveToMakeValid(s) {
    let a = [],
      b = [],
      c = [...s];
    for (let i = 0; i < c.length; i++) {
      if (c[i] == '(') a.push(i);
      else if (c[i] == ')') {
        if (a.length) a.pop();
        else b.push(i);
      }
    }
    for (let i of a) c[i] = '';
    for (let i of b) c[i] = '';
    return c.join('');
  }
}
```

## Contiguous Array

https://leetcode.com/problems/contiguous-array/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const findMaxLength = (nums) => {
  const n = nums.length;
  let a0 = Array(n + 1).fill(0);
  let a1 = Array(n + 1).fill(0);
  for (let i = 0; i < n; i++) {
    a0[i + 1] = a0[i] + (nums[i] == 0);
    a1[i + 1] = a1[i] + (nums[i] == 1);
  }
  for (let k = n; k >= 2; k--) {
    if (k & 1) continue;
    for (let i = 0; i + k <= n; i++) {
      if (a0[i + k] - a0[i] == a1[i + k] - a1[i]) return k;
    }
  }
  return 0;
};
```

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const findMaxLength = (nums) => {
  let a = new Map();
  a.set(0, -1);
  let b = 0,
    c = 0;
  for (let i = 0; i < nums.length; i++) {
    b += nums[i] ? 1 : -1;
    if (a.has(b)) c = Math.max(c, i - a.get(b));
    else a.set(b, i);
  }
  return c;
};
```

## Count Number of Bad Pairs

https://leetcode.com/problems/count-number-of-bad-pairs/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const countBadPairs = (nums) => {
  const n = nums.length;
  let a = {},
    b = 0;
  for (let i = 0; i < n; i++) a[nums[i] - i] = (a[nums[i] - i] ?? 0) + 1;
  for (let i in a) b += ((a[i] - 1) * a[i]) / 2;
  return ((n - 1) * n) / 2 - b;
};
```

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const countBadPairs = (nums) => {
  const n = nums.length;
  let a = {},
    b = 0;
  for (let i = 0; i < n; i++) {
    const c = nums[i] - i;
    b += a[c] ?? 0;
    a[c] = (a[c] ?? 0) + 1;
  }
  return ((n - 1) * n) / 2 - b;
};
```

## Find All Duplicates in an Array

https://leetcode.com/problems/find-all-duplicates-in-an-array/description/

```js
/**
 * @param {number[]} nums
 * @return {number[]}
 */
const findDuplicates = (nums) => {
  let a = {},
    b = [];
  for (let i of nums) {
    if (a[i]) b.push(i);
    a[i] = true;
  }
  return b;
};
```

## Find the Length of the Longest Common Prefix

https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/description/

```js
/**
 * @param {number[]} arr1
 * @param {number[]} arr2
 * @return {number}
 */
const longestCommonPrefix = (arr1, arr2) => {
  const a = new Set();
  for (let i of arr1) {
    const b = i + '';
    for (let j = 1; j <= b.length; j++) a.add(b.slice(0, j));
  }
  let c = 0;
  for (let i of arr2) {
    const b = i + '';
    for (let j = 1; j <= b.length; j++) {
      if (a.has(b.slice(0, j))) c = j > c ? j : c;
    }
  }
  return c;
};
```

## Count Unguarded Cells in the Grid

https://leetcode.com/problems/count-unguarded-cells-in-the-grid/description/

```js
/**
 * @param {number} m
 * @param {number} n
 * @param {number[][]} guards
 * @param {number[][]} walls
 * @return {number}
 */
const countUnguarded = (m, n, guards, walls) => {
  let g = new Set(guards.map(String));
  let w = new Set(walls.map(String));
  let a = 0;
  for (let y0 = 0; y0 < m; y0++) {
    for (let x0 = 0; x0 < n; x0++) {
      let b = false;

      let x = x0,
        y = y0;
      if (g.has(y + ',' + x) || w.has(y + ',' + x)) continue;

      while (x > 0) {
        x--;
        if (g.has(y + ',' + x)) {
          b = true;
          break;
        }
        if (w.has(y + ',' + x)) break;
      }
      if (b) continue;

      x = x0;
      while (x < n - 1) {
        x++;
        if (g.has(y + ',' + x)) {
          b = true;
          break;
        }
        if (w.has(y + ',' + x)) break;
      }
      if (b) continue;

      x = x0;
      while (y > 0) {
        y--;
        if (g.has(y + ',' + x)) {
          b = true;
          break;
        }
        if (w.has(y + ',' + x)) break;
      }
      if (b) continue;

      y = y0;
      while (y < m - 1) {
        y++;
        if (g.has(y + ',' + x)) {
          b = true;
          break;
        }
        if (w.has(y + ',' + x)) break;
      }
      if (b) continue;

      a++;
    }
  }
  return a;
};
```

```js
/**
 * @param {number} m
 * @param {number} n
 * @param {number[][]} guards
 * @param {number[][]} walls
 * @return {number}
 */
const countUnguarded = (m, n, guards, walls) => {
  let w = new Set(walls.map(String));
  let g = new Set();
  for (let [y0, x0] of guards) {
    let x = x0,
      y = y0;
    g.add(y + ',' + x);
    while (x > 0) {
      x--;
      if (w.has(y + ',' + x)) break;
      g.add(y + ',' + x);
    }
    x = x0;
    while (x < n - 1) {
      x++;
      if (w.has(y + ',' + x)) break;
      g.add(y + ',' + x);
    }
    x = x0;
    while (y > 0) {
      y--;
      if (w.has(y + ',' + x)) break;
      g.add(y + ',' + x);
    }
    y = y0;
    while (y < m - 1) {
      y++;
      if (w.has(y + ',' + x)) break;
      g.add(y + ',' + x);
    }
  }
  let b = g.union(w);
  let a = 0;
  for (let y = 0; y < m; y++) {
    for (let x = 0; x < n; x++) {
      if (!b.has(y + ',' + x)) a++;
    }
  }
  return a;
};
```

```js
/**
 * @param {number} m
 * @param {number} n
 * @param {number[][]} guards
 * @param {number[][]} walls
 * @return {number}
 */
const countUnguarded = (m, n, guards, walls) => {
  let w = new Set(walls.map(String));
  let g = Array.from({ length: m }, () => Array(n).fill(4));
  for (let [y, x] of guards) g[y][x] = 2;
  for (let [y, x] of walls) g[y][x] = 1;

  for (let y = 0; y < m; y++) {
    let a = false;
    for (let x = 0; x < n; x++) {
      if (g[y][x] == 2) a = true;
      else if (g[y][x] == 1) a = false;
      else if (a) g[y][x] = 0;
    }
    a = false;
    for (let x = n - 1; x >= 0; x--) {
      if (g[y][x] == 2) a = true;
      else if (g[y][x] == 1) a = false;
      else if (a) g[y][x] = 0;
    }
  }
  for (let x = 0; x < n; x++) {
    let a = false;
    for (let y = 0; y < m; y++) {
      if (g[y][x] == 2) a = true;
      else if (g[y][x] == 1) a = false;
      else if (a) g[y][x] = 0;
    }
    a = false;
    for (let y = m - 1; y >= 0; y--) {
      if (g[y][x] == 2) a = true;
      else if (g[y][x] == 1) a = false;
      else if (a) g[y][x] = 0;
    }
  }
  return g.flat().reduce((a, x) => a + (x >> 2), 0);
};
```

---

---

---

# Stack

## Min Stack

https://neetcode.io/problems/minimum-stack/question

```js
class MinStack {
  constructor() {
    this.a = [];
  }

  /**
   * @param {number} val
   * @return {void}
   */
  push(val) {
    this.a.push(val);
  }

  /**
   * @return {void}
   */
  pop() {
    this.a.pop();
  }

  /**
   * @return {number}
   */
  top() {
    return this.a.at(-1);
  }

  /**
   * @return {number}
   */
  getMin() {
    let b = Infinity;
    for (let i of this.a) b = i < b ? i : b;
    return b;
  }
}
```

## Evaluate Reverse Polish Notation

https://neetcode.io/problems/evaluate-reverse-polish-notation/question

```js
class Solution {
  /**
   * @param {string[]} tokens
   * @return {number}
   */
  evalRPN(tokens) {
    let a = [];
    for (let i of tokens) {
      if (i == '+') a.push(a.pop() + a.pop());
      else if (i == '-') a.push(-a.pop() + a.pop());
      else if (i == '*') a.push(a.pop() * a.pop());
      else if (i == '/') {
        const b = a.pop(),
          c = a.pop();
        a.push((c / b) | 0);
      } else a.push(+i);
    }
    return a[0];
  }
}
```

## Removing Stars from a String

https://leetcode.com/problems/removing-stars-from-a-string/description/

```js
/**
 * @param {string} s
 * @return {string}
 */
const removeStars = (s) => {
  let a = [];
  for (let i of s) {
    if (i == '*') a.pop();
    else a.push(i);
  }
  return a.join('');
};
```

## Validate Stack Ssequences

https://leetcode.com/problems/validate-stack-sequences/description/

```js
/**
 * @param {number[]} pushed
 * @param {number[]} popped
 * @return {boolean}
 */
const validateStackSequences = (pushed, popped) => {
  let a = [],
    b = 0;
  for (let i of pushed) {
    a.push(i);
    while (a.length && a.at(-1) == popped[b]) {
      a.pop();
      b++;
    }
  }
  return !a.length;
};
```

## Asteroid Collision

https://neetcode.io/problems/asteroid-collision/question

```js
class Solution {
  /**
   * @param {number[]} asteroids
   * @return {number[]}
   */
  asteroidCollision(asteroids) {
    let a = [];
    for (let i of asteroids) {
      let b = true;
      while (b && a.length && a.at(-1) > 0 && i < 0) {
        const c = a.at(-1);
        if (c < -i) a.pop();
        else if (c == -i) {
          a.pop();
          b = false;
        } else b = false;
      }
      if (b) a.push(i);
    }
    return a;
  }
}
```

## Daily Temperatures

https://neetcode.io/problems/daily-temperatures/question

```js
class Solution {
  /**
   * @param {number[]} temperatures
   * @return {number[]}
   */
  dailyTemperatures(temperatures) {
    const n = temperatures.length;
    let a = Array(n).fill(0),
      b = [];
    for (let i = 0; i < n; i++) {
      while (b.length && temperatures[i] > temperatures[b.at(-1)]) {
        const c = b.pop();
        a[c] = i - c;
      }
      b.push(i);
    }
    return a;
  }
}
```

## Online Stock Span

https://neetcode.io/problems/online-stock-span/question

```js
class StockSpanner {
  constructor() {
    this.a = [];
  }

  /**
   * @param {number} price
   * @return {number}
   */
  next(price) {
    let b = 1;
    while (this.a.length - b >= 0 && this.a.at(-b) <= price) b++;
    this.a.push(price);
    return b;
  }
}

/**
 * Your StockSpanner object will be instantiated and called as such:
 * var obj = new StockSpanner()
 * var param_1 = obj.next(price)
 */
```

## Car Fleet

https://neetcode.io/problems/car-fleet/question

```js
class Solution {
  /**
   * @param {number} target
   * @param {number[]} position
   * @param {number[]} speed
   * @return {number}
   */
  carFleet(target, position, speed) {
    let a = [];
    for (let i = 0; i < position.length; i++) {
      a.push([position[i], (target - position[i]) / speed[i]]);
    }
    a.sort((x1, x2) => x2[0] - x1[0]);
    let t0 = 0,
      b = 0;
    for (let [, t] of a) [t0, b] = t > t0 ? [t, b + 1] : [t0, b];
    return b;
  }
}
```

## Simplify Path

https://neetcode.io/problems/simplify-path/question

```js
class Solution {
  /**
   * @param {string} path
   * @return {string}
   */
  simplifyPath(path) {
    let a = [];
    for (let i of path.split('/')) {
      if (i == '' || i == '.') continue;
      if (i == '..') {
        if (a.length) a.pop();
      } else a.push(i);
    }
    return '/' + a.join('/');
  }
}
```

## Decode String

https://neetcode.io/problems/decode-string/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {string}
   */
  decodeString(s) {
    let a = [],
      b = [],
      c = '',
      k = 0;
    for (const i of s) {
      if (/\d/.test(i)) k = k * 10 + +i;
      else if (i == '[') {
        a.push(k);
        b.push(c);
        k = 0;
        c = '';
      } else if (i == ']') {
        const k0 = a.pop(),
          c0 = b.pop();
        c = c0 + c.repeat(k0);
      } else c += i;
    }
    return c;
  }
}
```

## Remove k Digits

https://leetcode.com/problems/remove-k-digits/description/

```js
/**
 * @param {string} num
 * @param {number} k
 * @return {string}
 */
const removeKdigits = (num, k) => {
  if (num.length == k) return '0';
  let a = [];
  for (let i of num) {
    while (k > 0 && a.length && a.at(-1) > i) {
      a.pop();
      k--;
    }
    a.push(i);
  }
  if (k) a = a.slice(0, -k);
  return a.join('').replace(/^0+/, '') || '0';
};
```

## Remove All Adjacent Duplicates In String II

https://neetcode.io/problems/remove-all-adjacent-duplicates-in-string-ii/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {number} k
   * @return {string}
   */
  removeDuplicates(s, k) {
    let a = [];
    for (let i of s) {
      a.push(i);
      let b = true;
      for (let j = 1; j < k; j++) {
        if (i != a.at(-j - 1)) {
          b = false;
          break;
        }
      }
      if (!b) continue;
      a = a.slice(0, -k);
    }
    return a.join('');
  }
}
```

```js
class Solution {
  /**
   * @param {string} s
   * @param {number} k
   * @return {string}
   */
  removeDuplicates(s, k) {
    let a = [];
    for (let i of s) {
      if (a.length && a.at(-1)[0] == i) a.at(-1)[1]++;
      else a.push([i, 1]);
      if (a.at(-1)[1] == k) a.pop();
    }
    let b = '';
    for (let [i, c] of a) b += i.repeat(c);
    return b;
  }
}
```

## Reverse Substrings Between Each Pair of Parentheses

https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/description/

```js
/**
 * @param {string} s
 * @return {string}
 */
const reverseParentheses = (s) => {
  let a = [],
    c = '';
  for (let i of s) {
    if (i == '(') {
      a.push(c);
      c = '';
    } else if (i == ')') c = a.pop() + c.split('').reverse().join('');
    else c += i;
  }
  return c;
};
```

```js
/**
 * @param {string} s
 * @return {string}
 */
const reverseParentheses = (s) => {
  const n = s.length;
  let a = Array(n);
  let b = [];
  for (let i = 0; i < n; i++) {
    if (s[i] == '(') b.push(i);
    else if (s[i] === ')') {
      const j = b.pop();
      a[i] = j;
      a[j] = i;
    }
  }
  let c = [],
    i = 0,
    d = 1;
  while (i < n) {
    if (s[i] == '(' || s[i] == ')') [i, d] = [a[i], -d];
    else c.push(s[i]);
    i += d;
  }
  return c.join('');
};
```

## Minimum Add to Make Parentheses Valid

https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const minAddToMakeValid = (s) => {
  let l = 0,
    r = 0;
  for (let i of s) {
    if (i == '(') l++;
    else if (i == ')') {
      if (l > 0) l--;
      else r++;
    }
  }
  return l + r;
};
```

## Maximum Width Ramp

https://leetcode.com/problems/maximum-width-ramp/description/

```js
/**
 * @param {number[]} nums
 * @return {number}
 */
const maxWidthRamp = (nums) => {
  let n = nums.length;
  let a = [0];
  for (let i = 0; i < n; i++) {
    if (nums[i] < nums[a.at(-1)]) a.push(i);
  }
  let b = 0;
  for (let i = n - 1; i >= 0; i--) {
    while (a.length && nums[a.at(-1)] <= nums[i]) b = Math.max(i - a.pop(), b);
  }
  return b;
};
```

## Basic Calculator II

https://neetcode.io/problems/basic-calculator-ii/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  calculate(s) {
    s = s.replaceAll(' ', '');
    let a = [],
      b = 0;
    for (let i of s) {
      if (/\d/.test(i)) b = +i + b * 10;
      else {
        a.push(b);
        b = 0;
        a.push(i);
      }
    }
    a.push(b);
    b = [];
    for (let i = 0; i < a.length; i++) {
      if (a[i] == '*') {
        b.push(b.pop() * a[i + 1]);
        i++;
      } else if (a[i] == '/') {
        b.push((b.pop() / a[i + 1]) | 0);
        i++;
      } else b.push(a[i]);
    }
    let c = b[0];
    for (let i = 1; i < b.length; i += 2) {
      c += b[i] == '+' ? b[i + 1] : -b[i + 1];
    }
    return c;
  }
}
```

## 132 Pattern

https://leetcode.com/problems/132-pattern/description/

```js
/**
 * @param {number[]} nums
 * @return {boolean}
 */
const find132pattern = (nums) => {
  let a = [],
    b = -Infinity;
  for (let i of nums.reverse()) {
    if (i < b) return true;
    while (a.length && i > a.at(-1)) b = a.pop();
    a.push(i);
  }
  return false;
};
```

## Flatten Nested List Iterator

https://leetcode.com/problems/flatten-nested-list-iterator/description/

```js
/**
 * // This is the interface that allows for creating nested lists.
 * // You should not implement it, or speculate about its implementation
 * function NestedInteger() {
 *
 *     Return true if this NestedInteger holds a single integer, rather than a nested list.
 *     @return {boolean}
 *     this.isInteger = function() {
 *         ...
 *     };
 *
 *     Return the single integer that this NestedInteger holds, if it holds a single integer
 *     Return null if this NestedInteger holds a nested list
 *     @return {integer}
 *     this.getInteger = function() {
 *         ...
 *     };
 *
 *     Return the nested list that this NestedInteger holds, if it holds a nested list
 *     Return null if this NestedInteger holds a single integer
 *     @return {NestedInteger[]}
 *     this.getList = function() {
 *         ...
 *     };
 * };
 */
/**
 * @constructor
 * @param {NestedInteger[]} nestedList
 */
const NestedIterator = function(nestedList) {
    this.arr = [];
    const dfs = list => {
        for (const x of list) {
            if (x.isInteger()) this.arr.push(x.getInteger();
            else dfs(x.getList();
        }
    };
    dfs(nestedList);
    this.idx = 0;
};

// const NestedIterator = function(nestedList) {
//     const str='['+JSON.stringify(nestedList).replace(/(\[|\])/g,'')+']';
//     this.arr=JSON.parse(str);
//     this.idx = 0;
// };

/**
 * @this NestedIterator
 * @returns {boolean}
 */
NestedIterator.prototype.hasNext = function() {
    return this.idx < this.arr.length;
};

/**
 * @this NestedIterator
 * @returns {integer}
 */
NestedIterator.prototype.next = function() {
    return this.arr[this.idx++];
};

/**
 * Your NestedIterator will be called like this:
 * var i = new NestedIterator(nestedList), a = [];
 * while (i.hasNext()) a.push(i.next());
*/
```

## Sum of Subarray minimums

https://leetcode.com/problems/sum-of-subarray-minimums/description/

```js
/**
 * @param {number[]} arr
 * @return {number}
 */
const sumSubarrayMins = (arr) => {
  const M = 1e9 + 7;
  let a = 0;
  for (let i = 0; i < arr.length; i++) {
    const b = arr[i];
    let l = i,
      r = i;
    while (l > 0 && arr[l - 1] > b) l--;
    while (r < arr.length - 1 && arr[r + 1] >= b) r++;
    a = (a + b * (i - l + 1) * (r - i + 1)) % M;
  }
  return a;
};
```

```js
/**
 * @param {number[]} arr
 * @return {number}
 */
const sumSubarrayMins = (arr) => {
  const M = 1e9 + 7;
  const n = arr.length;
  let a = 0;
  let b = [];
  for (let i = 0; i <= n; i++) {
    while (b.length && (i == n || arr[b.at(-1)] >= arr[i])) {
      const m = b.pop();
      const l = b.length ? b.at(-1) : -1;
      const r = i;
      const c = (m - l) * (r - m);
      a = (a + arr[m] * c) % M;
    }
    b.push(i);
  }
  return a;
};
```

---

---

---

# Two Pointers

## Adding Spaces to a String

https://leetcode.com/problems/adding-spaces-to-a-string/description/

```js
/**
 * @param {string} s
 * @param {number[]} spaces
 * @return {string}
 */
const addSpaces = (s, spaces) => {
  let a = '',
    i0 = 0;
  for (let i of spaces) {
    a += s.slice(i0, i) + ' ';
    i0 = i;
  }
  return a + s.slice(i0);
};
```

## String Compression

https://neetcode.io/problems/string-compression/question

```js
class Solution {
  /**
   * @param {character[]} chars
   * @return {number}
   */
  compress(chars) {
    let i1 = 0,
      i2 = 0;
    while (i1 < chars.length) {
      const a = chars[i1];
      let b = 0;
      while (i1 < chars.length && chars[i1] == a) {
        i1++;
        b++;
      }
      chars[i2++] = a;
      if (b > 1) {
        for (let i of b + '') chars[i2++] = i;
      }
    }
    chars.length = i2;
    return i2;
  }
}
```

## Remove Duplicates From Sorted Array II

https://neetcode.io/problems/remove-duplicates-from-sorted-array-ii/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number}
   */
  removeDuplicates(nums) {
    if (nums.length <= 2) return nums.length;
    let i0 = 2;
    for (let i = 2; i < nums.length; i++) {
      if (nums[i] != nums[i0 - 2]) nums[i0++] = nums[i];
    }
    return i0;
  }
}
```

## Partition Array According to Given Pivot

https://leetcode.com/problems/partition-array-according-to-given-pivot/description/

```js
/**
 * @param {number[]} nums
 * @param {number} pivot
 * @return {number[]}
 */
const pivotArray = (nums, pivot) => {
  let a1 = [],
    a2 = [],
    a3 = [];
  for (let i of nums) {
    if (i < pivot) a1.push(i);
    else if (i > pivot) a3.push(i);
    else a2.push(i);
  }
  return [...a1, ...a2, ...a3];
};
```

## Two Integer Sum II

https://neetcode.io/problems/two-integer-sum-ii/question

```js
class Solution {
  /**
   * @param {number[]} numbers
   * @param {number} target
   * @return {number[]}
   */
  twoSum(numbers, target) {
    for (let i = 0; i < numbers.length; i++) {
      const k = numbers.indexOf(target - numbers[i]);
      if (k > -1 && k != i) return [i + 1, k + 1];
    }
  }
}
```

## 3Sum

https://neetcode.io/problems/three-integer-sum/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[][]}
   */
  threeSum(nums) {
    let a = new Set();
    let ap = [],
      an = [],
      z = 0;
    for (let i of nums) {
      if (i > 0) ap.push(i);
      else if (i < 0) an.push(i);
      else z++;
    }
    const sp = new Set(ap);
    const sn = new Set(an);

    if (z > 2) a.add('0,0,0');
    if (z > 0) {
      for (let p of ap) {
        if (sn.has(-p)) a.add(-p + ',' + p + ',0');
      }
    }

    for (let i = 0; i < ap.length - 1; i++) {
      for (let j = i + 1; j < ap.length; j++) {
        const n = -ap[i] - ap[j];
        if (sn.has(n)) a.add([ap[i], ap[j], n].sort().join(','));
      }
    }
    for (let i = 0; i < an.length - 1; i++) {
      for (let j = i + 1; j < an.length; j++) {
        const p = -an[i] - an[j];
        if (sp.has(p)) a.add([an[i], an[j], p].sort().join(','));
      }
    }

    return [...a].map((x) => x.split(',').map(Number));
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[][]}
   */
  threeSum(nums) {
    nums.sort((x1, x2) => x1 - x2);
    const a = [];
    for (let i = 0; i < nums.length - 2; i++) {
      if (i > 0 && nums[i] == nums[i - 1]) continue;
      let l = i + 1,
        r = nums.length - 1;
      while (l < r) {
        const b = nums[i] + nums[l] + nums[r];
        if (b < 0) l++;
        else if (b > 0) r--;
        else {
          a.push([nums[i], nums[l], nums[r]]);
          l++;
          r--;
          while (l < r && nums[l] == nums[l - 1]) l++;
          while (l < r && nums[r] == nums[r + 1]) r--;
        }
      }
    }
    return a;
  }
}
```

## 4Sum

https://neetcode.io/problems/4sum/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number[][]}
   */
  fourSum(nums, target) {
    nums.sort((x1, x2) => x1 - x2);
    const a = [],
      n = nums.length;
    for (let i = 0; i < n - 3; i++) {
      if (i > 0 && nums[i] == nums[i - 1]) continue;
      for (let j = i + 1; j < n - 2; j++) {
        if (j > i + 1 && nums[j] == nums[j - 1]) continue;
        let l = j + 1,
          r = n - 1;
        while (l < r) {
          const b = nums[i] + nums[j] + nums[l] + nums[r];
          if (b < target) l++;
          else if (b > target) r--;
          else {
            a.push([nums[i], nums[j], nums[l], nums[r]]);
            l++;
            r--;
            while (l < r && nums[l] == nums[l - 1]) l++;
            while (l < r && nums[r] == nums[r + 1]) r--;
          }
        }
      }
    }
    return a;
  }
}
```

## Rotate Array

https://neetcode.io/problems/rotate-array/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {void} Do not return anything, modify nums in-place instead.
   */
  rotate(nums, k) {
    const n = nums.length;
    k %= n;
    nums.unshift(...nums.splice(n - k, k));
  }
}
```

## Container With Most Water

https://neetcode.io/problems/max-water-container/question

```js
class Solution {
  /**
   * @param {number[]} heights
   * @return {number}
   */
  maxArea(heights) {
    let a = 0;
    let l = 0,
      r = heights.length - 1;
    while (l < r) {
      const h = Math.min(heights[l], heights[r]);
      a = Math.max(a, h * (r - l));
      [l, r] = heights[l] < heights[r] ? [l + 1, r] : [l, r - 1];
    }
    return a;
  }
}
```

## Number of Subsequences That Satisfy The Given Sum Condition

https://neetcode.io/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} target
   * @return {number}
   */
  numSubseq(nums, target) {
    const M = 1e9 + 7;
    const n = nums.length;
    const pow2 = Array(n).fill(1);
    for (let i = 1; i < n; i++) pow2[i] = (pow2[i - 1] * 2) % M;

    nums.sort((x1, x2) => x1 - x2);
    let a = 0,
      l = 0,
      r = n - 1;
    while (l <= r) {
      if (nums[l] + nums[r] <= target) {
        a = (a + pow2[r - l]) % M;
        l++;
      } else r--;
    }
    return a;
  }
}
```

## Array with Elements not Equal to Average of Neighbors

https://leetcode.com/problems/array-with-elements-not-equal-to-average-of-neighbors/description/

```js
/**
 * @param {number[]} nums
 * @return {number[]}
 */
const rearrangeArray = (nums) => {
  const n = nums.length;
  nums.sort((x1, x2) => x1 - x2);
  for (let i = 1; i < n - 1; i += 2) [nums[i], nums[i + 1]] = [nums[i + 1], nums[i]];
  return nums;
};
```

## Divide Players Into Teams of Equal Skill

https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/description/

```js
/**
 * @param {number[]} skill
 * @return {number}
 */
const dividePlayers = (skill) => {
  skill.sort((x1, x2) => x1 - x2);
  const a = skill[0] + skill.at(-1);
  let b = 0;
  for (let i = 0; i < skill.length / 2; i++) {
    const c = skill[i] + skill.at(-1 - i);
    if (c != a) return -1;
    b += skill[i] * skill.at(-1 - i);
  }
  return b;
};
```

## Boats to Save People

https://neetcode.io/problems/boats-to-save-people/question

```js
class Solution {
  /**
   * @param {number[]} people
   * @param {number} limit
   * @return {number}
   */
  numRescueBoats(people, limit) {
    people.sort((x1, x2) => x1 - x2);
    let a = 0,
      l = 0,
      r = people.length - 1;
    while (l <= r) {
      if (people[l] + people[r] <= limit) l++;
      r--;
      a++;
    }
    return a;
  }
}
```

## K-th Symbol in Grammar

https://leetcode.com/problems/k-th-symbol-in-grammar/description/

```js
/**
 * @param {number} n
 * @param {number} k
 * @return {number}
 */
const kthGrammar = (n, k) => {
  let a = [false];
  for (let i = 0; i < n; i++) {
    for (let ii = 0; ii < 2 ** i; ii++) a.push(!a[ii]);
  }
  return a[k - 1] ? 1 : 0;
};
```

```js
/**
 * @param {number} n
 * @param {number} k
 * @return {number}
 */
const kthGrammar = (n, k) => {
  k--;
  let a = 0;
  while (k) {
    a += k & 1;
    k >>= 1;
  }
  return a % 2;
};
```

## Minimum Time to Make Rope Colorful

https://leetcode.com/problems/minimum-time-to-make-rope-colorful/description/

```js
/**
 * @param {string} colors
 * @param {number[]} neededTime
 * @return {number}
 */
const minCost = (colors, neededTime) => {
  let a = 0,
    b = neededTime[0],
    c = b,
    d = colors[0];
  for (let i = 1; i < colors.length; i++) {
    if (colors[i] != d) {
      a += b - c;
      b = neededTime[i];
      c = b;
      d = colors[i];
    } else {
      b += neededTime[i];
      c = Math.max(neededTime[i], c);
    }
  }
  return a + b - c;
};
```

## Rearrange Array Elements by Sign

https://neetcode.io/problems/rearrange-array-elements-by-sign/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @return {number[]}
   */
  rearrangeArray(nums) {
    let a = [],
      i1 = 0,
      i2 = 1;
    for (let i of nums) {
      if (i > 0) [a[i1], i1] = [i, i1 + 2];
      else [a[i2], i2] = [i, i2 + 2];
    }
    return a;
  }
}
```

## Bag of Tokens

https://leetcode.com/problems/bag-of-tokens/description/

```js
/**
 * @param {number[]} tokens
 * @param {number} power
 * @return {number}
 */
const bagOfTokensScore = (tokens, power) => {
  tokens.sort((x1, x2) => x1 - x2);
  let l = 0,
    r = tokens.length - 1,
    a0 = 0,
    a = 0;
  while (l <= r) {
    if (power >= tokens[l]) {
      a++;
      a0 = Math.max(a, a0);
      power -= tokens[l++];
    } else if (a > 0) {
      a--;
      power += tokens[r--];
    } else break;
  }
  return a0;
};
```

## Minimum Length of String After Deleting Similar Ends

https://leetcode.com/problems/minimum-length-of-string-after-deleting-similar-ends/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const minimumLength = (s) => {
  let l = 0,
    r = s.length - 1;
  while (s[l] == s[r] && l < r) {
    const a = s[l];
    while (s[l] == a && l <= r) l++;
    while (s[r] == a && l < r) r--;
  }
  return r - l + 1;
};
```

## Sentence Similarity III

https://leetcode.com/problems/sentence-similarity-iii/description/

```js
/**
 * @param {string} sentence1
 * @param {string} sentence2
 * @return {boolean}
 */
const areSentencesSimilar = (sentence1, sentence2) => {
  if (sentence1 == sentence2) return true;
  let s1 = sentence1.split(' '),
    s2 = sentence2.split(' ');
  if (s1.length < s2.length) [s1, s2] = [s2, s1];
  let a = 0;
  while (s1[a] == s2[a]) a++;
  let b = 1;
  while (s1.at(-b) == s2.at(-b)) b++;
  return a + b - 1 >= s2.length;
};
```

---

---

---

# Sliding Window

## Number of Sub Arrays of Size K and Avg Greater than or Equal to Threshold

https://neetcode.io/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/question

```js
class Solution {
  /**
   * @param {number[]} arr
   * @param {number} k
   * @param {number} threshold
   * @return {number}
   */
  numOfSubarrays(arr, k, threshold) {
    let a = arr.slice(0, k).reduce((a, x) => a + x, 0),
      b = 0;
    for (let i = 0; i <= arr.length - k; i++) {
      b += a >= threshold * k ? 1 : 0;
      a += -arr[i] + arr[i + k];
    }
    return b;
  }
}
```

## Grumpy Bookstore Owner

https://neetcode.io/problems/grumpy-bookstore-owner/question

```js
class Solution {
  /**
   * @param {number[]} customers
   * @param {number[]} grumpy
   * @param {number} minutes
   * @return {number}
   */
  maxSatisfied(customers, grumpy, minutes) {
    const m = minutes;
    let a0 = 0;
    for (let i = 0; i < m; i++) a0 += customers[i] * !grumpy[i];
    let b = customers.slice(0, m).reduce((a, x) => a + x, 0);
    let a = a0,
      c = b - a;
    for (let i = m; i < customers.length; i++) {
      a0 += customers[i] * !grumpy[i];
      a += -customers[i - m] * !grumpy[i - m] + customers[i] * !grumpy[i];
      b += -customers[i - m] + customers[i];
      c = b - a > c ? b - a : c;
    }
    return a0 + c;
  }
}
```

## Alternating Groups II

https://leetcode.com/problems/alternating-groups-ii/description/

```js
/**
 * @param {number[]} colors
 * @param {number} k
 * @return {number}
 */
const numberOfAlternatingGroups = (colors, k) => {
  const n = colors.length;
  let a = 0,
    b = 1;
  for (let i = 1; i < n + k - 1; i++) {
    if (colors[i % n] != colors[(i - 1) % n]) b++;
    else b = 1;
    a += b >= k ? 1 : 0;
  }
  return a;
};
```

## Longest Substring Without Repeating Characters

https://neetcode.io/problems/longest-substring-without-duplicates/question

```js
class Solution {
  /**
   * @param {string} s
   * @return {number}
   */
  lengthOfLongestSubstring(s) {
    let a = {},
      l = 0,
      b = 0;
    for (let i = 0; i < s.length; i++) {
      if (s[i] in a) l = Math.max(l, a[s[i]] + 1);
      a[s[i]] = i;
      b = Math.max(b, i - l + 1);
    }
    return b;
  }
}
```

## Longest Repeating Character Replacement

https://neetcode.io/problems/longest-repeating-substring-with-replacement/question

```js
class Solution {
  /**
   * @param {string} s
   * @param {number} k
   * @return {number}
   */
  characterReplacement(s, k) {
    let a = {},
      l = 0,
      b = 0,
      c = 0;
    for (let r = 0; r < s.length; r++) {
      a[s[r]] = (a[s[r]] || 0) + 1;
      b = Math.max(a[s[r]], b);
      while (r - l + 1 - b > k) {
        a[s[l]]--;
        l++;
      }
      c = Math.max(r - l + 1, c);
    }
    return c;
  }
}
```

## Permutation in String

https://neetcode.io/problems/permutation-string/question

```js
class Solution {
  /**
   * @param {string} s1
   * @param {string} s2
   * @return {boolean}
   */
  checkInclusion(s1, s2) {
    const n = s1.length;
    const a = [...s1].sort().join('');
    for (let i = 0; i <= s2.length - n; i++) {
      if ([...s2.slice(i, i + n)].sort().join('') == a) return true;
    }
    return false;
  }
}
```

```js
class Solution {
  /**
   * @param {string} s1
   * @param {string} s2
   * @return {boolean}
   */
  checkInclusion(s1, s2) {
    const n = s1.length;
    const a1 = Array(26).fill(0),
      a2 = Array(26).fill(0);
    for (const i of s1) a1[i.charCodeAt(0) - 97]++;
    for (let i = 0; i < s2.length; i++) {
      a2[s2.charCodeAt(i) - 97]++;
      if (i >= n) a2[s2.charCodeAt(i - n) - 97]--;
      if (a1.join() == a2.join()) return true;
    }
    return false;
  }
}
```

## Frequency of The Most Frequent Element

https://neetcode.io/problems/frequency-of-the-most-frequent-element/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  maxFrequency(nums, k) {
    nums.sort((x1, x2) => x1 - x2);
    let a = 0,
      b = 1,
      l = 0;
    for (let r = 1; r < nums.length; r++) {
      a += (nums[r] - nums[r - 1]) * (r - l);
      while (a > k) a -= nums[r] - nums[l++];
      b = Math.max(r - l + 1, b);
    }
    return b;
  }
}
```

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  maxFrequency(nums, k) {
    nums.sort((x1, x2) => x1 - x2);
    let a = 0,
      b = 0,
      l = 0;
    for (let r = 0; r < nums.length; r++) {
      a += nums[r];
      while (nums[r] * (r - l + 1) - a > k) a -= nums[l++];
      b = Math.max(r - l + 1, b);
    }
    return b;
  }
}
```

## Fruits into Basket

https://neetcode.io/problems/fruit-into-baskets/question

```js
class Solution {
  /**
   * @param {number[]} fruits
   * @return {number}
   */
  totalFruit(fruits) {
    let a = {},
      b = 0,
      c = 0,
      l = 0;
    for (let r = 0; r < fruits.length; r++) {
      c += a[fruits[r]] ? 0 : 1;
      a[fruits[r]] = (a[fruits[r]] ?? 0) + 1;
      while (c > 2) {
        a[fruits[l]]--;
        if (a[fruits[l]] == 0) {
          delete a[fruits[l]];
          c--;
        }
        l++;
      }
      b = Math.max(r - l + 1, b);
    }
    return b;
  }
}
```

## Maximum Number of Vowels in a Substring of Given Length

https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/

```js
/**
 * @param {string} s
 * @param {number} k
 * @return {number}
 */
const maxVowels = (s, k) => {
  const re = /[aeiou]/;
  let a = 0;
  for (let i = 0; i < k; i++) a += re.test(s[i]) ? 1 : 0;
  let a0 = a;
  for (let i = k; i < s.length; i++) {
    a += -(re.test(s[i - k]) ? 1 : 0) + (re.test(s[i]) ? 1 : 0);
    a0 = a > a0 ? a : a0;
  }
  return a0;
};
```

## Minimum Number of Flips to Make the Binary String Alternating

https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const minFlips = (s) => {
  const n = s.length,
    ss = s + s;
  let a1 = 0,
    a2 = 0,
    a = n;
  for (let i = 0; i < ss.length; i++) {
    const c1 = i % 2,
      c2 = 1 - c1;
    if (+ss[i] != c1) a1++;
    if (+ss[i] != c2) a2++;
    if (i >= n) {
      const d1 = (i - n) % 2,
        d2 = 1 - d1;
      if (+ss[i - n] != d1) a1--;
      if (+ss[i - n] != d2) a2--;
    }
    if (i >= n - 1) a = Math.min(a, a1, a2);
  }
  return a;
};
```

```js
/**
 * @param {string} s
 * @return {number}
 */
const minFlips = (s) => {
  const n = s.length,
    ss = s + s;
  let a0 = n,
    a = 0;
  for (let i = 0; i < ss.length; i++) {
    if (+ss[i] != i % 2) a++;
    if (i >= n && +ss[i - n] != (i - n) % 2) a--;
    if (i >= n - 1) a0 = Math.min(a0, a, n - a);
  }
  return a0;
};
```

## Minimum Size Subarray Sum

https://neetcode.io/problems/minimum-size-subarray-sum/question

```js
class Solution {
  /**
   * @param {number} target
   * @param {number[]} nums
   * @return {number}
   */
  minSubArrayLen(target, nums) {
    let a = Infinity,
      b = 0,
      i0 = 0;
    for (let i = 0; i < nums.length; i++) {
      b += nums[i];
      while (b >= target) {
        a = Math.min(i - i0 + 1, a);
        b -= nums[i0++];
      }
    }
    return a != Infinity ? a : 0;
  }
}
```

## Find K Closest Elements

https://neetcode.io/problems/find-k-closest-elements/question

```js
class Solution {
  /**
   * @param {number[]} arr
   * @param {number} k
   * @param {number} x
   * @return {number[]}
   */
  findClosestElements(arr, k, x) {
    return arr
      .sort((x1, x2) => Math.abs(x1 - x) - Math.abs(x2 - x))
      .slice(0, k)
      .sort((x1, x2) => x1 - x2);
  }
}
```

## Minimum Operations to Reduce x to Zero

https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/description/

```js
/**
 * @param {number[]} nums
 * @param {number} x
 * @return {number}
 */
const minOperations = (nums, x) => {
  const n = nums.length;
  let al = [0],
    ar = [0],
    a = Infinity;
  for (let i of nums) al.push(al.at(-1) + i);
  for (let i of nums.reverse()) ar.push(ar.at(-1) + i);
  for (let i = 0; i <= n; i++) {
    const b = ar.indexOf(x - al[i]);
    if (b >= 0 && b <= n - i) a = Math.min(i + b, a);
  }
  return a != Infinity ? a : -1;
};
```

```js
/**
 * @param {number[]} nums
 * @param {number} x
 * @return {number}
 */
const minOperations = (nums, x) => {
  const n = nums.length,
    a = nums.reduce((a, x) => a + x, 0) - x;
  if (a < 0) return -1;
  else if (!a) return n;
  let b = 0,
    l = 0,
    c = -1;
  for (let r = 0; r < n; r++) {
    b += nums[r];
    while (b > a) b -= nums[l++];
    if (b == a) c = Math.max(r - l + 1, c);
  }
  return c == -1 ? -1 : n - c;
};
```

## Get Equal Substrings Within Budget

https://leetcode.com/problems/get-equal-substrings-within-budget/description/

```js
/**
 * @param {string} s
 * @param {string} t
 * @param {number} maxCost
 * @return {number}
 */
const equalSubstring = (s, t, maxCost) => {
  let a = 0,
    b = 0,
    i0 = 0;
  for (let i = 0; i < s.length; i++) {
    a += Math.abs(s[i].charCodeAt(0) - t[i].charCodeAt(0));
    while (a > maxCost) {
      a -= Math.abs(s[i0].charCodeAt(0) - t[i0].charCodeAt(0));
      i0++;
    }
    b = Math.max(i - i0 + 1, b);
  }
  return b;
};
```

## Number of Substrings Containing All Three Characters

https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/description/

```js
/**
 * @param {string} s
 * @return {number}
 */
const numberOfSubstrings = (s) => {
  let n = { a: 0, b: 0, c: 0 },
    a = 0,
    l = 0;
  for (let r = 0; r < s.length; r++) {
    n[s[r]]++;
    while (n.a && n.b && n.c) {
      a += s.length - r;
      n[s[l++]]--;
    }
  }
  return a;
};
```

## Binary Subarrays with Sum

https://neetcode.io/problems/binary-subarrays-with-sum/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} goal
   * @return {number}
   */
  numSubarraysWithSum(nums, goal) {
    let c = new Map([[0, 1]]),
      a = 0,
      b = 0;
    for (let i of nums) {
      a += i;
      b += c.get(a - goal) || 0;
      c.set(a, (c.get(a) || 0) + 1);
    }
    return b;
  }
}
```

## Count Number of Nice Subarrays

https://leetcode.com/problems/count-number-of-nice-subarrays/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const numberOfSubarrays = (nums, k) => {
  let c = new Map([[0, 1]]),
    a = 0,
    b = 0;
  for (let i of nums) {
    a += i & 1;
    b += c.get(a - k) || 0;
    c.set(a, (c.get(a) || 0) + 1);
  }
  return b;
};
```

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const numberOfSubarrays = (nums, k) => {
  let a = [-1];
  for (let i = 0; i < nums.length; i++) {
    if (nums[i] & 1) a.push(i);
  }
  a.push(nums.length);
  let b = 0;
  for (let i = 1; i + k - 1 < a.length - 1; i++) {
    b += (a[i] - a[i - 1]) * (a[i + k] - a[i + k - 1]);
  }
  return b;
};
```

## Subarray Product Less Than K

https://neetcode.io/problems/subarray-product-less-than-k/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  numSubarrayProductLessThanK(nums, k) {
    let a = 0,
      b,
      l = 0,
      r = 0;
    while (l < nums.length) {
      ((b = nums[l]), (r = l));
      while (b < k) {
        a++;
        r++;
        b *= nums[r];
      }
      l++;
    }
    return a;
  }
}
```

## Max Consecutive Ones III

https://neetcode.io/problems/max-consecutive-ones-iii/question

```js
class Solution {
  /**
   * @param {number[]} nums
   * @param {number} k
   * @return {number}
   */
  longestOnes(nums, k) {
    let a = 0,
      b = 0,
      l = 0;
    for (let r = 0; r < nums.length; r++) {
      if (nums[r] == 0) b++;
      while (b > k) b -= nums[l++] == 0 ? 1 : 0;
      a = Math.max(r - l + 1, a);
    }
    return a;
  }
}
```

## Find the Power of K-Size Subarrays I

https://leetcode.com/problems/find-the-power-of-k-size-subarrays-i/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number[]}
 */
const resultsArray = (nums, k) => {
  if (k == 1) return nums;
  let a = [],
    b = 1;
  for (let i = 1; i < nums.length; i++) {
    if (nums[i] == nums[i - 1] + 1) b++;
    else b = 1;
    if (i >= k - 1) a.push(b >= k ? nums[i] : -1);
  }
  return a;
};
```

## Maximum Sum of Distinct Subarrays With Length K

https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const maximumSubarraySum = (nums, k) => {
  let a = {},
    b = 0,
    c = 0,
    d = 0;
  for (let i of nums.slice(0, k)) {
    if (!(i in a)) d++;
    a[i] = (a[i] ?? 0) + 1;
    b += i;
  }
  if (d == k) c = b;
  for (let i = k; i < nums.length; i++) {
    const e0 = nums[i - k],
      e1 = nums[i];
    b += -e0 + e1;
    if (!(e1 in a)) d++;
    a[e1] = (a[e1] ?? 0) + 1;
    a[e0]--;
    if (a[e0] == 0) {
      delete a[e0];
      d--;
    }
    if (d == k) c = b > c ? b : c;
  }
  return c;
};
```

## Length of Longest Subarray With at Most K Frequency

https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const maxSubarrayLength = (nums, k) => {
  let a = {},
    b = 1,
    l = 0,
    r = 0;
  while (r < nums.length) {
    const c = nums[r];
    a[c] = (a[c] ?? 0) + 1;
    while (a[c] > k) a[nums[l++]]--;
    b = Math.max(r - l + 1, b);
    r++;
  }
  return b;
};
```

## Count Subarrays Where Max Element Appears at Least K Times

https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const countSubarrays = (nums, k) => {
  const n = nums.length,
    a = Math.max(...nums);
  let b = 0,
    c = 0,
    l = 0;
  for (let r = 0; r < n; r++) {
    b += nums[r] == a ? 1 : 0;
    while (b >= k) {
      c += n - r;
      b -= nums[l++] == a ? 1 : 0;
    }
  }
  return c;
};
```

## Maximum Beauty of an Array After Applying Operation

https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const maximumBeauty = (nums, k) => {
  let a = {};
  for (let i of nums) {
    for (let ii = i - k; ii <= i + k; ii++) a[ii] = (a[ii] ?? 0) + 1;
  }
  return Math.max(...Object.values(a));
};
```

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const maximumBeauty = (nums, k) => {
  nums.sort((x1, x2) => x1 - x2);
  let a = 0,
    l = 0;
  for (let r = 0; r < nums.length; r++) {
    while (nums[r] - nums[l] > 2 * k) l++;
    a = Math.max(r - l + 1, a);
  }
  return a;
};
```

## Take K of Each Character From Left and Right

https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/description/

```js
/**
 * @param {string} s
 * @param {number} k
 * @return {number}
 */
const takeCharacters = (s, k) => {
  const n = s.length;
  let a = { a: 0, b: 0, c: 0 },
    b = { a: 0, b: 0, c: 0 },
    c = 0,
    l = 0,
    r = 0;
  for (let i of s) a[i]++;
  if (a.a < k || a.b < k || a.c < k) return -1;
  for (let r = 0; r < n; r++) {
    const d = s[r];
    b[d]++;
    while (b[d] > a[d] - k) b[s[l++]]--;
    c = Math.max(r - l + 1, c);
  }
  return n - c;
};
```

## Count of Substrings Containing Every Vowel and K Consonants II

https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/description/

```js
/**
 * @param {string} word
 * @param {number} k
 * @return {number}
 */
const countOfSubstrings = (word, k) => {
  const fn = (k) => {
    if (k < 0) return 0;
    let a = { a: -1, e: -1, i: -1, o: -1, u: -1 },
      b = 0,
      c = 0,
      l = 0;
    for (let r = 0; r < word.length; r++) {
      const d = word[r];
      if ('aeiou'.includes(d)) a[d] = r;
      else b++;
      while (b > k) {
        if (!'aeiou'.includes(word[l])) b--;
        l++;
      }
      const e = Math.min(a.a, a.e, a.i, a.o, a.u);
      if (e >= l) c += e - l + 1;
    }
    return c;
  };
  return fn(k) - fn(k - 1);
};
```

## Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

https://neetcode.io/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/question

```js

```

---

---

---

# Binary Search

## Single Element in a Sorted Array

https://neetcode.io/problems/single-element-in-a-sorted-array/question

```js

```

## Find Peak Element

https://neetcode.io/problems/find-peak-element/question

```js

```

## Successful Pairs of Spells and Potions

https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/

```js

```

## Search a 2D Matrix

https://neetcode.io/problems/search-2d-matrix/question

```js

```

## Koko Eating Bananas

https://neetcode.io/problems/eating-bananas/question

```js

```

## Capacity to Ship Packages Within D Days

https://neetcode.io/problems/capacity-to-ship-packages-within-d-days/question

```js

```

## Maximum Candies Allocated to K Children

https://leetcode.com/problems/maximum-candies-allocated-to-k-children/description/

```js
/**
 * @param {number[]} candies
 * @param {number} k
 * @return {number}
 */
const maximumCandies = (candies, k) => {
  if (candies.reduce((a, x) => a + x, 0) < k) return 0;
  let l = 1,
    r = Math.max(...candies);
  while (l < r) {
    const m = (l + r + 1) >> 1;
    [l, r] = candies.reduce((a, x) => a + ((x / m) | 0), 0) >= k ? [m, r] : [l, m - 1];
  }
  return l;
};
```

## House Robber IV

https://leetcode.com/problems/house-robber-iv/description/

```js
/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
const minCapability = (nums, k) => {
  let l = Math.min(...nums),
    r = Math.max(...nums);
  const check = (cap) => {
    let cnt = 0;
    for (let i = 0; i < nums.length; ) {
      [cnt, i] = nums[i] <= cap ? [cnt + 1, i + 2] : [cnt, i + 1];
    }
    return cnt >= k;
  };

  while (l < r) {
    const m = (l + r) >> 1;
    [l, r] = check(m) ? [l, m] : [m + 1, r];
  }
  return l;
};
```

## Minimized Maximum of Products Distributed to Any Store

https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/description/

```js
/**
 * @param {number} n
 * @param {number[]} quantities
 * @return {number}
 */
const minimizedMaximum = (n, quantities) => {
  let l = 1,
    r = Math.max(...quantities);
  while (l < r) {
    const m = (l + r) >> 1;
    [l, r] = quantities.reduce((a, x) => a + (((x + m - 1) / m) | 0), 0) > n ? [m + 1, r] : [l, m];
  }
  return l;
};
```

## Minimum Limit of Balls in a Bag

https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/description/

```js
/**
 * @param {number[]} nums
 * @param {number} maxOperations
 * @return {number}
 */
const minimumSize = (nums, maxOperations) => {
  let l = 1,
    r = Math.max(...nums);
  while (l < r) {
    const m = (l + r) >> 1;
    let a = 0;
    for (let i of nums) a += ((i - 1) / m) | 0;
    [l, r] = a > maxOperations ? [m + 1, r] : [l, m];
  }
  return l;
};
```

## Minimum Time to Repair Cars

https://leetcode.com/problems/minimum-time-to-repair-cars/description/

```js
/**
 * @param {number[]} ranks
 * @param {number} cars
 * @return {number}
 */
const repairCars = (ranks, cars) => {
  let l = 0,
    r = Math.min(...ranks) * cars ** 2;
  while (l < r) {
    const m = Math.floor((l + r) / 2);
    let a = 0;
    for (const i of ranks) a += ((m / i) ** 0.5) | 0;
    [l, r] = a < cars ? [m + 1, r] : [l, m];
  }
  return l;
};
```

## Find Minimum in Rotated Sorted Array

https://neetcode.io/problems/find-minimum-in-rotated-sorted-array/question

```js

```

## Search in Rotated Sorted Array

https://neetcode.io/problems/find-target-in-rotated-sorted-array/question

```js

```

## Search in Rotated Sorted Array II

https://neetcode.io/problems/search-in-rotated-sorted-array-ii/question

```js

```

## Time Based Key-Value Store

https://neetcode.io/problems/time-based-key-value-store/question

```js

```

## Find First And Last Position of Element In Sorted Array

https://neetcode.io/problems/find-first-and-last-position-of-element-in-sorted-array/question

```js

```

## Maximum Number of Removable Characters

https://leetcode.com/problems/maximum-number-of-removable-characters/description/

```js
/**
 * @param {string} s
 * @param {string} p
 * @param {number[]} removable
 * @return {number}
 */
const maximumRemovals = (s, p, removable) => {
  const a = Array(s.length).fill(Infinity);
  for (let i = 0; i < removable.length; i++) a[removable[i]] = i;
  const check = (k) => {
    let j = 0;
    for (let i = 0; i < s.length && j < p.length; i++) {
      if (a[i] < k) continue;
      if (s[i] == p[j]) j++;
    }
    return j == p.length;
  };

  let l = 0,
    r = removable.length + 1;
  while (l < r) {
    const m = (l + r) >> 1;
    [l, r] = check(m) ? [m + 1, r] : [l, m];
  }
  return l - 1;
};
```

## Most Beautiful Item for Each Query

https://leetcode.com/problems/most-beautiful-item-for-each-query/description/

```js
/**
 * @param {number[][]} items
 * @param {number[]} queries
 * @return {number[]}
 */
const maximumBeauty = (items, queries) => {
  items.sort((x1, x2) => x1[0] - x2[0]);
  for (let i = 1; i < items.length; i++) items[i][1] = Math.max(items[i][1], items[i - 1][1]);
  let a = [];
  for (let i of queries) {
    let l = 0,
      r = items.length;
    while (l < r) {
      const m = (l + r) >> 1;
      [l, r] = items[m][0] <= i ? [m + 1, r] : [l, m];
    }
    a.push(l ? items[l - 1][1] : 0);
  }
  return a;
};
```

```js
/**
 * @param {number[][]} items
 * @param {number[]} queries
 * @return {number[]}
 */
const maximumBeauty = (items, queries) => {
  items.sort((x1, x2) => x1[0] - x2[0]);
  const qs = queries.map((q, i) => [q, i]);
  qs.sort((x1, x2) => x1[0] - x2[0]);
  let a = Array(queries.length);
  let i = 0,
    b = 0;
  for (let [q, id] of qs) {
    while (i < items.length && items[i][0] <= q) b = Math.max(items[i++][1], b);
    a[id] = b;
  }
  return a;
};
```

## Random Pick with Weight

https://neetcode.io/problems/random-pick-with-weight/question

```js

```

## Search Suggestions System

https://leetcode.com/problems/search-suggestions-system/description/

```js

```

## Count the Number of Fair Pairs

https://leetcode.com/problems/count-the-number-of-fair-pairs/description/

```js

```

---

---

---

# Linked List

##
