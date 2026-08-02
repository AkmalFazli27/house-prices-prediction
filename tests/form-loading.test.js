const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const loadingScript = fs.readFileSync(
  path.join(__dirname, "..", "app", "static", "js", "form_loading.js"),
  "utf8",
);

function createFormEnvironment() {
  const handlers = {};
  const changes = [];
  const label = { textContent: "Predict" };
  const idleIcon = {
    classList: {
      add: (name) => changes.push(["idle-add", name]),
    },
  };
  const spinner = {
    classList: {
      remove: (name) => changes.push(["spinner-remove", name]),
    },
  };
  const button = {
    disabled: false,
    dataset: {},
    querySelector: (selector) => {
      if (selector === ".btn-label") return label;
      if (selector === ".btn-predict-icon") return idleIcon;
      if (selector === ".btn-predict-spinner") return spinner;
      return null;
    },
    setAttribute: (name, value) => changes.push(["attribute", name, value]),
  };
  const form = {
    addEventListener: (event, handler) => {
      handlers[event] = handler;
    },
    querySelector: (selector) => selector === ".btn-predict" ? button : null,
  };
  const context = {
    document: {
      querySelectorAll: (selector) => selector === "form" ? [form] : [],
    },
  };

  vm.runInNewContext(loadingScript, context);
  return { button, changes, handlers, label, spinner };
}

function testEntersLoadingState() {
  const { button, changes, handlers, label } = createFormEnvironment();

  handlers.submit({ defaultPrevented: false });

  assert.equal(button.disabled, true);
  assert.equal(label.textContent, "Predicting...");
  assert.deepEqual(changes, [
    ["attribute", "aria-busy", "true"],
    ["idle-add", "hidden"],
    ["spinner-remove", "hidden"],
  ]);
}

function testIgnoresDuplicateSubmit() {
  const { button, changes, handlers } = createFormEnvironment();

  handlers.submit({ defaultPrevented: false });
  const firstChangeCount = changes.length;
  handlers.submit({ defaultPrevented: false });

  assert.equal(button.disabled, true);
  assert.equal(changes.length, firstChangeCount);
}

function testIgnoresCancelledSubmit() {
  const { button, changes, handlers } = createFormEnvironment();

  handlers.submit({ defaultPrevented: true });

  assert.equal(button.disabled, false);
  assert.deepEqual(changes, []);
}

const tests = [
  ["enters the prediction loading state", testEntersLoadingState],
  ["ignores duplicate submits while loading", testIgnoresDuplicateSubmit],
  ["ignores a submit already cancelled by validation", testIgnoresCancelledSubmit],
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
