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

  const context = {
    document: {
      documentElement: { scrollHeight },
      querySelectorAll: (selector) => {
        if (selector === ".detail-section") return sections;
        if (selector === ".detail-sidebar-item") return navItems;
        return [];
      },
      getElementById: () => null,
    },
    window: {
      innerHeight: 800,
      scrollY,
      addEventListener: () => {},
    },
  };

  vm.runInNewContext(detailScript, context);
  return activeSections;
}

function testKeepsOutdoorFeaturesActive() {
  const activeSections = runScrollSpy({
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
  const activeSections = runScrollSpy({
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

const tests = [
  [
    "keeps Outdoor Features active when Sale Information is visible but page is not at bottom",
    testKeepsOutdoorFeaturesActive,
  ],
  ["activates Sale Information when the document is at the bottom", testActivatesSaleInformationAtBottom],
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
