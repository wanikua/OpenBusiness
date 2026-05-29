const demoProfiles = {
  saas: {
    market: "B2B Developer Platform",
    funding: "Series C+",
    moat: "Moderate",
    outlook: "Positive",
    counts: { verified: 18, inferred: 41, missing: 9 },
  },
  "ai-infra": {
    market: "AI Infrastructure",
    funding: "Growth",
    moat: "Moderate",
    outlook: "Mixed",
    counts: { verified: 16, inferred: 48, missing: 13 },
  },
  "public-company": {
    market: "Public Company",
    funding: "Public",
    moat: "Strong",
    outlook: "Positive",
    counts: { verified: 32, inferred: 18, missing: 5 },
  },
  "consumer-app": {
    market: "B2C / Prosumer",
    funding: "Series B",
    moat: "Weak",
    outlook: "Mixed",
    counts: { verified: 14, inferred: 46, missing: 16 },
  },
  ecommerce: {
    market: "DTC / Marketplace",
    funding: "Not found",
    moat: "Weak",
    outlook: "Unknown",
    counts: { verified: 12, inferred: 33, missing: 22 },
  },
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const stageItems = $$("#pipelineList li");
const activeStage = $("#activeStage");
const runStatus = $("#runStatus");
const pipelineProgress = $("#pipelineProgress");
const packSelect = $("#packSelect");
const templateSelect = $("#templateSelect");
const companyInput = $("#companyInput");
const domainInput = $("#domainInput");

function safeGsap(callback) {
  if (!window.gsap) {
    return;
  }
  callback(window.gsap);
}

function iconRefresh() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function setProfile(profileKey) {
  const profile = demoProfiles[profileKey] || demoProfiles.saas;
  $("#marketType").textContent = profile.market;
  $("#fundingStage").textContent = profile.funding;
  $("#moatVerdict").textContent = profile.moat;
  $("#outlookVerdict").textContent = profile.outlook;
  animateCounts(profile.counts);
}

function animateCounts(counts) {
  const total = counts.verified + counts.inferred + counts.missing;
  const model = { verified: 0, inferred: 0, missing: 0 };

  safeGsap((gsap) => {
    gsap.to(model, {
      verified: counts.verified,
      inferred: counts.inferred,
      missing: counts.missing,
      duration: 0.8,
      ease: "power2.out",
      onUpdate: () => {
        $("#verifiedCount").textContent = Math.round(model.verified);
        $("#inferredCount").textContent = Math.round(model.inferred);
        $("#missingCount").textContent = Math.round(model.missing);
      },
    });
    gsap.to("#verifiedFill", {
      width: `${(counts.verified / total) * 100}%`,
      duration: 0.8,
      ease: "power2.out",
    });
    gsap.to("#inferredFill", {
      width: `${(counts.inferred / total) * 100}%`,
      duration: 0.8,
      ease: "power2.out",
    });
    gsap.to("#missingFill", {
      width: `${(counts.missing / total) * 100}%`,
      duration: 0.8,
      ease: "power2.out",
    });
  });

  if (!window.gsap) {
    $("#verifiedCount").textContent = counts.verified;
    $("#inferredCount").textContent = counts.inferred;
    $("#missingCount").textContent = counts.missing;
    $("#verifiedFill").style.width = `${(counts.verified / total) * 100}%`;
    $("#inferredFill").style.width = `${(counts.inferred / total) * 100}%`;
    $("#missingFill").style.width = `${(counts.missing / total) * 100}%`;
  }
}

function resetStages() {
  stageItems.forEach((item) => {
    item.classList.remove("running", "done");
    item.querySelector(".stage-state").textContent = "queued";
  });
  activeStage.textContent = "idle";
  runStatus.textContent = "Ready";
  pipelineProgress.style.transform = "scaleX(0)";

  safeGsap((gsap) => {
    gsap.set(stageItems, { y: 0, scale: 1, autoAlpha: 1, clearProps: "transform" });
    gsap.set(".verdict-row, .canvas-grid div, .metric-tile", { clearProps: "all" });
    gsap.set(pipelineProgress, { scaleX: 0, transformOrigin: "left center" });
  });
}

function runDemo() {
  resetStages();
  runStatus.textContent = "Running";
  const company = companyInput.value.trim() || "Vercel";
  const domain = domainInput.value.trim() || "vercel.com";
  $("#reportTitle").textContent = `${company} business model`;

  safeGsap((gsap) => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const duration = reduceMotion ? 0.01 : 0.22;
    const tl = gsap.timeline({ defaults: { duration, ease: "power2.out" } });

    tl.to(pipelineProgress, { scaleX: 1, duration: reduceMotion ? 0.01 : 2.8, ease: "power1.inOut" }, 0);

    stageItems.forEach((item, index) => {
      const state = item.querySelector(".stage-state");
      const label = item.dataset.stage;
      tl.addLabel(`stage-${index}`, index * 0.23);
      tl.call(
        () => {
          stageItems.forEach((stage) => stage.classList.remove("running"));
          item.classList.add("running");
          state.textContent = "running";
          activeStage.textContent = label;
        },
        null,
        `stage-${index}`,
      );
      tl.fromTo(item, { y: 8, scale: 0.985 }, { y: 0, scale: 1 }, `stage-${index}`);
      tl.call(
        () => {
          item.classList.remove("running");
          item.classList.add("done");
          state.textContent = "done";
        },
        null,
        `stage-${index}+=0.2`,
      );
    });

    tl.call(() => {
      activeStage.textContent = "finalized";
      runStatus.textContent = "Complete";
    });
    tl.from(".verdict-row", { y: 12, autoAlpha: 0, stagger: 0.08, duration: 0.35 }, "-=0.2");
    tl.from(".canvas-grid div", { y: 10, autoAlpha: 0, stagger: 0.05, duration: 0.28 }, "<0.1");
    tl.fromTo(".metric-tile", { y: 8 }, { y: 0, stagger: 0.04, duration: 0.24 }, "<");
  });

  if (!window.gsap) {
    stageItems.forEach((item) => {
      item.classList.add("done");
      item.querySelector(".stage-state").textContent = "done";
    });
    activeStage.textContent = `${company} on ${domain}`;
    runStatus.textContent = "Complete";
  }
}

function setTab(tab) {
  $$(".artifact-item").forEach((button) => button.classList.toggle("active", button.dataset.tab === tab));
  $$(".tab-panel").forEach((panel) => panel.classList.toggle("active", panel.id === `tab-${tab}`));

  safeGsap((gsap) => {
    gsap.fromTo(`#tab-${tab}`, { y: 10, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.24 });
  });
}

function setupCursorLight() {
  safeGsap((gsap) => {
    const light = $(".cursor-light");
    const xTo = gsap.quickTo(light, "x", { duration: 0.45, ease: "power3" });
    const yTo = gsap.quickTo(light, "y", { duration: 0.45, ease: "power3" });

    window.addEventListener("pointermove", (event) => {
      gsap.to(light, { autoAlpha: 1, duration: 0.25 });
      xTo(event.clientX);
      yTo(event.clientY);
    });
  });
}

function init() {
  iconRefresh();
  setProfile(packSelect.value);
  resetStages();
  setupCursorLight();

  packSelect.addEventListener("change", () => {
    setProfile(packSelect.value);
    safeGsap((gsap) => {
      gsap.fromTo(".metric-tile", { y: 8, autoAlpha: 0.5 }, { y: 0, autoAlpha: 1, stagger: 0.05 });
    });
  });

  templateSelect.addEventListener("change", () => {
    $(".json-preview code").textContent = `{
  "analysis_pack": "${packSelect.value}",
  "report_template": "${templateSelect.value}",
  "claim_contract": ["VERIFIED", "INFERRED", "MISSING"],
  "artifacts": {
    "report": "report.en.md",
    "sources": "sources.md",
    "stages": 9
  }
}`;
  });

  $("#runDemo").addEventListener("click", runDemo);
  $("#resetDemo").addEventListener("click", resetStages);
  $$(".artifact-item").forEach((button) => {
    button.addEventListener("click", () => setTab(button.dataset.tab));
  });

  safeGsap((gsap) => {
    gsap.defaults({ ease: "power2.out" });
    gsap.from(".topbar", { y: -12, autoAlpha: 0, duration: 0.4 });
    gsap.from(".control-rail, .pipeline-panel, .report-pane", {
      y: 14,
      autoAlpha: 0,
      stagger: 0.08,
      duration: 0.45,
    });
  });
}

document.addEventListener("DOMContentLoaded", init);
