const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const detailScript = fs.readFileSync(
  path.join(__dirname, "..", "app", "static", "js", "detail.js"),
  "utf8",
);

function runScrollSpy({ scrollY, scrollHeight, sectionRects }) {
  const activeSections = new Map();
  const buttonState = { hidden: true };
  const buttonHandlers = {};
  const scrollCalls = [];
  const sections = sectionRects.map(([id, rect]) => ({
    id: `section-${id}`,
    getBoundingClientRect: () => rect,
  }));
  const navItems = sectionRects.map(([id]) => ({
    dataset: { section: id },
    addEventListener: () => {},
    classList: {
      toggle: (_className, isActive) => activeSections.set(id, isActive),
    },
  }));
  const backToTop = {
    classList: {
      toggle: (className, isHidden) => {
        if (className === "hidden") buttonState.hidden = isHidden;
      },
    },
    addEventListener: (event, handler) => {
      buttonHandlers[event] = handler;
    },
  };

  const context = {
    document: {
      documentElement: { scrollHeight },
      querySelectorAll: (selector) => {
        if (selector === ".detail-section") return sections;
        if (selector === ".detail-sidebar-item") return navItems;
        return [];
      },
      getElementById: (id) => id === "back-to-top" ? backToTop : null,
    },
    window: {
      innerHeight: 800,
      scrollY,
      addEventListener: () => {},
      scrollTo: (options) => scrollCalls.push(options),
    },
  };

  vm.runInNewContext(detailScript, context);
  return { activeSections, buttonState, buttonHandlers, scrollCalls };
}

function testKeepsOutdoorFeaturesActive() {
  const { activeSections } = runScrollSpy({
    scrollY: 400,
    scrollHeight: 1800,
    sectionRects: [
      ["lot_location", { top: -700, bottom: -400 }],
      ["outdoor_features", { top: 100, bottom: 450 }],
      ["sale_information", { top: 500, bottom: 650 }],
    ],
  });

  assert.equal(activeSections.get("outdoor_features"), true);
  assert.equal(activeSections.get("sale_information"), false);
}

function testActivatesSaleInformationAtBottom() {
  const { activeSections } = runScrollSpy({
    scrollY: 1000,
    scrollHeight: 1800,
    sectionRects: [
      ["lot_location", { top: -1300, bottom: -1000 }],
      ["outdoor_features", { top: -500, bottom: -150 }],
      ["sale_information", { top: 20, bottom: 180 }],
    ],
  });

  assert.equal(activeSections.get("sale_information"), true);
  assert.equal(activeSections.get("outdoor_features"), false);
}

function testBackToTopIsHiddenBeforeThreshold() {
  const { buttonState } = runScrollSpy({
    scrollY: 299,
    scrollHeight: 1800,
    sectionRects: [],
  });

  assert.equal(buttonState.hidden, true);
}

function testBackToTopIsVisibleAfterThreshold() {
  const { buttonState } = runScrollSpy({
    scrollY: 300,
    scrollHeight: 1800,
    sectionRects: [],
  });

  assert.equal(buttonState.hidden, false);
}

function testBackToTopUsesSmoothScroll() {
  const { buttonHandlers, scrollCalls } = runScrollSpy({
    scrollY: 400,
    scrollHeight: 1800,
    sectionRects: [],
  });

  assert.equal(typeof buttonHandlers.click, "function");
  buttonHandlers.click();
  assert.equal(scrollCalls.length, 1);
  assert.equal(scrollCalls[0].top, 0);
  assert.equal(scrollCalls[0].behavior, "smooth");
}

const tests = [
  [
    "keeps Outdoor Features active when Sale Information is visible but page is not at bottom",
    testKeepsOutdoorFeaturesActive,
  ],
  ["activates Sale Information when the document is at the bottom", testActivatesSaleInformationAtBottom],
  ["keeps the back-to-top button hidden before the scroll threshold", testBackToTopIsHiddenBeforeThreshold],
  ["shows the back-to-top button after the scroll threshold", testBackToTopIsVisibleAfterThreshold],
  ["uses smooth scrolling when the back-to-top button is clicked", testBackToTopUsesSmoothScroll],
];

let failures = 0;
for (const [name, testCase] of tests) {
  try {
    testCase();
    console.log(`PASS ${name}`);
  } catch (error) {
    failures += 1;
    console.error(`FAIL ${name}`);
    console.error(error.message);
  }
}

if (failures > 0) process.exitCode = 1;
