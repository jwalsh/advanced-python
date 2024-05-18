const car = (lst: any[]): any => lst[0];

const cdr = (lst: any[]): any[] | null => {
  if (lst.length === 1) {
    return null;
  } else {
    return lst.slice(1);
  }
};

/**
 * Checks if a given element is a member of a list using recursion.
 * @param {any} x - The element to search for in the list.
 * @param {any[]} lst - The list to search for the element.
 * @returns {boolean} - Returns true if the element is found in the list, false otherwise.
 */
const memberP = (x: any, lst: any[]): boolean => {
  if (lst === null) {
    return false;
  } else if (x === car(lst)) {
    return true;
  } else {
    return memberP(x, cdr(lst));
  }
};

const memberPTests = [
  {
    name: "Three is a member of the list",
    inputX: 3,
    inputLst: [1, 2, 3, 4, 5],
    expected: true,
  },
  {
    name: "Three is not a member of the list",
    inputX: 3,
    inputLst: [1, 2, 4, 5],
    expected: false,
  },
  {
    name: "Three is not a member of an empty list",
    inputX: 3,
    inputLst: [],
    expected: false,
  },
  {
    name: "Three is a member of a list with only three",
    inputX: 3,
    inputLst: [3],
    expected: true,
  },
  {
    name: "Three is not a member of a list with only four",
    inputX: 3,
    inputLst: [4],
    expected: false,
  },
  {
    name: "Three is not a member of a null list",
    inputX: 3,
    inputLst: null,
    expected: false,
  },
];

for (const test of memberPTests) {
  const expected = test.expected;
  const result = memberP(test.inputX, test.inputLst);
  console.assert(expected === result, test.name);
}

/**
 * Checks if a given element is a member of a list using a loop.
 * @param {any} x - The element to search for in the list.
 * @param {any[]} lst - The list to search for the element.
 * @returns {boolean} - Returns true if the element is found in the list, false otherwise.
 */
const memberPLoop = (x: any, lst: any[]): boolean => {
  if (lst === null) {
    return false;
  } else {
    for (let i = 0; i < lst.length; i++) {
      if (x === lst[i]) {
        return true;
      }
    }
    return false;
  }
};

/**
 * Checks if a given element is a member of a list using the reduce function.
 * @param {any} x - The element to search for in the list.
 * @param {any[]} lst - The list to search for the element.
 * @returns {boolean} - Returns true if the element is found in the list, false otherwise.
 */
const memberPReduce = (x: any, lst: any[]): boolean => {
  return reduce((acc: boolean, y: any) => {
    return acc || y === x;
  }, false, lst);
};
