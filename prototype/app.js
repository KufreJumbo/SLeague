const state = {
  view: "dashboard",
  subject: "Mathematics",
  term: "Term 1",
  xp: 2840,
  streak: 5,
  rank: 4,
  boardMode: "overall",
  quiz: {
    index: 0,
    selected: null,
    score: 0,
    activeTopic: "Fractions",
  },
};

const subjects = {
  Mathematics: {
    mastery: 76,
    note: "You are strongest in whole numbers. Fractions and measurement need attention.",
    terms: {
      "Term 1": [
        { title: "Whole numbers", status: "Completed", score: 91 },
        { title: "Fractions", status: "Recommended", score: 62 },
        { title: "Measurement", status: "Practice due", score: 68 },
        { title: "Simple equations", status: "Locked", score: 0 },
      ],
      "Term 2": [
        { title: "Decimals", status: "Ready", score: 0 },
        { title: "Ratio and proportion", status: "Ready", score: 0 },
        { title: "Angles", status: "Ready", score: 0 },
      ],
      "Term 3": [
        { title: "Perimeter and area", status: "Ready", score: 0 },
        { title: "Statistics", status: "Ready", score: 0 },
        { title: "Coordinates", status: "Ready", score: 0 },
      ],
    },
  },
  English: {
    mastery: 82,
    note: "Comprehension is strong. Grammar drills will help protect your subject rank.",
    terms: {
      "Term 1": [
        { title: "Parts of speech", status: "Completed", score: 88 },
        { title: "Comprehension", status: "Completed", score: 92 },
        { title: "Letter writing", status: "Practice due", score: 70 },
      ],
      "Term 2": [
        { title: "Tenses", status: "Ready", score: 0 },
        { title: "Summary writing", status: "Ready", score: 0 },
      ],
      "Term 3": [
        { title: "Oral English", status: "Ready", score: 0 },
        { title: "Essay writing", status: "Ready", score: 0 },
      ],
    },
  },
  "Basic Science": {
    mastery: 71,
    note: "Living things is secure. Energy transfer needs a quick recovery session.",
    terms: {
      "Term 1": [
        { title: "Living things", status: "Completed", score: 84 },
        { title: "Energy", status: "Recommended", score: 59 },
        { title: "Matter", status: "Practice due", score: 66 },
      ],
      "Term 2": [
        { title: "Simple machines", status: "Ready", score: 0 },
        { title: "Health science", status: "Ready", score: 0 },
      ],
      "Term 3": [
        { title: "The solar system", status: "Ready", score: 0 },
        { title: "Environmental science", status: "Ready", score: 0 },
      ],
    },
  },
  "Social Studies": {
    mastery: 79,
    note: "Civic topics are improving. Revise map reading before the weekly challenge.",
    terms: {
      "Term 1": [
        { title: "Family and community", status: "Completed", score: 86 },
        { title: "Map reading", status: "Recommended", score: 65 },
        { title: "Culture", status: "Practice due", score: 72 },
      ],
      "Term 2": [
        { title: "Leadership", status: "Ready", score: 0 },
        { title: "National values", status: "Ready", score: 0 },
      ],
      "Term 3": [
        { title: "Resources", status: "Ready", score: 0 },
        { title: "Transport", status: "Ready", score: 0 },
      ],
    },
  },
};

const questions = [
  {
    prompt: "Which fraction is equivalent to 1/2?",
    options: ["2/3", "3/6", "4/5", "1/3"],
    answer: "3/6",
    explanation: "Multiplying numerator and denominator by 3 gives 3/6.",
  },
  {
    prompt: "What is 1/4 + 1/4?",
    options: ["1/8", "1/4", "1/2", "2/8"],
    answer: "1/2",
    explanation: "The denominators are the same, so 1 + 1 = 2. Two quarters make one half.",
  },
  {
    prompt: "Convert 7/4 to a mixed number.",
    options: ["1 3/4", "2 1/4", "3 1/4", "1 1/4"],
    answer: "1 3/4",
    explanation: "7 divided by 4 is 1 remainder 3, so the mixed number is 1 3/4.",
  },
];

let leaders = [
  { name: "Amara Bello", xp: 3210, score: 93, tier: "Platinum" },
  { name: "Chinedu Obi", xp: 3025, score: 89, tier: "Gold" },
  { name: "Musa Danjuma", xp: 2910, score: 86, tier: "Gold" },
  { name: "Ada Okafor", xp: state.xp, score: 84, tier: "Gold", current: true },
  { name: "Kemi Adebayo", xp: 2620, score: 78, tier: "Silver" },
  { name: "Tari Ebi", xp: 2480, score: 75, tier: "Silver" },
];

const tasks = [
  { title: "Fractions checkpoint", detail: "Mathematics - 10 adaptive questions", tag: "+120 XP" },
  { title: "Letter writing practice", detail: "English - teacher-style feedback", tag: "+80 XP" },
  { title: "Energy revision", detail: "Basic Science - weak topic recovery", tag: "+95 XP" },
];

const challenges = [
  {
    title: "Fractions Sprint",
    subject: "Mathematics",
    reward: "+300 XP",
    status: "Active now",
    copy: "Score above 85% before Friday to enter the class top-five challenge board.",
  },
  {
    title: "Grammar Guard",
    subject: "English",
    reward: "+180 XP",
    status: "2 days left",
    copy: "Beat your previous tense and punctuation score with one timed attempt.",
  },
  {
    title: "Science Recall",
    subject: "Basic Science",
    reward: "+220 XP",
    status: "Opens Monday",
    copy: "A fast recall round on energy, matter, and living things.",
  },
];

const titles = {
  dashboard: "Home Dashboard",
  subjects: "Subject Hub",
  tutor: "AI Tutor Chat",
  leaderboard: "Leaderboard",
  insights: "Performance Insights",
  challenges: "Challenges Arena",
};

const viewTitle = document.getElementById("viewTitle");
const subjectFilter = document.getElementById("subjectFilter");
const quizModal = document.getElementById("quizModal");
const quizBody = document.getElementById("quizBody");

function formatNumber(value) {
  return new Intl.NumberFormat("en-NG").format(value);
}

function renderDashboard() {
  document.getElementById("dashboardRank").textContent = state.rank;
  document.getElementById("xpValue").textContent = formatNumber(state.xp);
  document.getElementById("streakValue").textContent = `${state.streak} days`;
  document.getElementById("tierValue").textContent = state.xp >= 3000 ? "Platinum" : "Gold";
  document.getElementById("xpProgress").style.width = `${Math.min((state.xp % 1000) / 10, 100)}%`;

  document.getElementById("taskList").innerHTML = tasks
    .map(
      (task) => `
        <article class="task-item">
          <div>
            <strong>${task.title}</strong>
            <span>${task.detail}</span>
          </div>
          <span class="status-pill">${task.tag}</span>
        </article>
      `,
    )
    .join("");

  document.getElementById("leaderMini").innerHTML = getSortedLeaders()
    .slice(0, 4)
    .map(
      (student, index) => `
        <div class="leader-row">
          <div>
            <span class="rank-chip">${index + 1}</span>
            <strong>${student.name}</strong>
          </div>
          <span>${formatNumber(student.xp)} XP</span>
        </div>
      `,
    )
    .join("");
}

function renderSubjects() {
  const subject = subjects[state.subject];
  const topics = subject.terms[state.term];
  document.getElementById("subjectHeading").textContent = state.subject;
  document.getElementById("masteryScore").textContent = `${subject.mastery}%`;
  document.getElementById("masteryNote").textContent = subject.note;
  document.getElementById("masteryDonut").style.background =
    `conic-gradient(var(--teal) 0 ${subject.mastery}%, var(--mist) ${subject.mastery}% 100%)`;

  document.querySelectorAll(".term-tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.term === state.term);
  });

  document.getElementById("topicList").innerHTML = topics
    .map(
      (topic) => `
        <article class="topic-row">
          <div>
            <strong>${topic.title}</strong>
            <span>${state.term} - ${topic.status}</span>
          </div>
          <div class="topic-score">${topic.score ? `${topic.score}%` : "--"}</div>
          <button class="text-button start-topic" data-topic="${topic.title}" type="button">
            ${topic.status === "Locked" ? "Preview" : "Practice"}
          </button>
        </article>
      `,
    )
    .join("");

  document.querySelectorAll(".start-topic").forEach((button) => {
    button.addEventListener("click", () => openQuiz(button.dataset.topic));
  });
}

function renderTutor() {
  document.getElementById("tutorSubject").textContent = `${state.subject} Tutor`;
  const chatLog = document.getElementById("chatLog");
  if (!chatLog.dataset.started) {
    chatLog.dataset.started = "true";
    chatLog.innerHTML = `
      <div class="message bot">
        I am ready to help with ${state.subject}. Ask for a simple explanation, an exam example,
        or a revision plan based on your scores.
      </div>
    `;
  }
}

function getSortedLeaders() {
  return [...leaders].sort((a, b) => b.xp - a.xp);
}

function renderLeaderboard() {
  document.querySelectorAll(".segment").forEach((segment) => {
    segment.classList.toggle("active", segment.dataset.board === state.boardMode);
  });

  document.getElementById("leaderboardTable").innerHTML = getSortedLeaders()
    .map((student, index) => {
      const score = state.boardMode === "overall" ? `${formatNumber(student.xp)} XP` : `${student.score}%`;
      return `
        <div class="leader-table-row">
          <div class="student-cell">
            <span class="rank-chip">${index + 1}</span>
            <div>
              <strong>${student.name}${student.current ? " - you" : ""}</strong>
              <span>${student.tier} League</span>
            </div>
          </div>
          <strong class="score-cell">${score}</strong>
        </div>
      `;
    })
    .join("");
}

function renderInsights() {
  const nextRank = state.rank <= 3 ? "Likely to keep a top-three finish" : "Likely to finish 3rd this term";
  document.getElementById("predictionTitle").textContent = nextRank;
  document.getElementById("predictionText").textContent =
    state.xp >= 3000
      ? "Your recent quiz streak has moved you into a promotion path. Keep the pace through this week."
      : "Two more Mathematics wins and one English practice streak could move you ahead of Chinedu.";

  const values = [58, 64, 61, 72, 70, 78, 82, Math.min(94, 84 + Math.floor((state.xp - 2840) / 20))];
  document.getElementById("trendChart").innerHTML = values
    .map((value) => `<div class="trend-bar" style="height:${value}%"></div>`)
    .join("");

  document.getElementById("recoveryList").innerHTML = [
    ["Fractions", "Retake the checkpoint and review mixed numbers."],
    ["Measurement", "Complete two practice sets before Friday."],
    ["Letter writing", "Revise formal letter structure and closing lines."],
  ]
    .map(
      ([title, detail]) => `
        <article class="recovery-item">
          <strong>${title}</strong>
          <span>${detail}</span>
        </article>
      `,
    )
    .join("");
}

function renderChallenges() {
  document.getElementById("challengeGrid").innerHTML = challenges
    .map(
      (challenge, index) => `
        <article class="challenge-card ${index === 0 ? "active" : ""}">
          <div>
            <p class="eyebrow">${challenge.subject}</p>
            <h2>${challenge.title}</h2>
            <p>${challenge.copy}</p>
          </div>
          <div class="challenge-meta">
            <span>${challenge.status}</span>
            <strong>${challenge.reward}</strong>
          </div>
          <button class="primary-action challenge-start" data-subject="${challenge.subject}" type="button">
            Enter challenge
          </button>
        </article>
      `,
    )
    .join("");

  document.querySelectorAll(".challenge-start").forEach((button) => {
    button.addEventListener("click", () => {
      state.subject = button.dataset.subject;
      subjectFilter.value = state.subject;
      openQuiz(challenges.find((item) => item.subject === state.subject)?.title || "Challenge");
    });
  });
}

function renderCurrentView() {
  viewTitle.textContent = titles[state.view];
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active-view"));
  document.getElementById(`${state.view}View`).classList.add("active-view");

  renderDashboard();
  renderSubjects();
  renderTutor();
  renderLeaderboard();
  renderInsights();
  renderChallenges();
}

function setView(view) {
  state.view = view;
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.view === view);
  });
  renderCurrentView();
}

function openQuiz(topic) {
  state.quiz = { index: 0, selected: null, score: 0, activeTopic: topic };
  document.getElementById("quizTitle").textContent = `${topic} Checkpoint`;
  document.getElementById("quizMeta").textContent = `${state.subject} - adaptive test`;
  quizModal.classList.add("open");
  quizModal.setAttribute("aria-hidden", "false");
  renderQuizQuestion();
}

function closeQuiz() {
  quizModal.classList.remove("open");
  quizModal.setAttribute("aria-hidden", "true");
}

function renderQuizQuestion() {
  const question = questions[state.quiz.index];
  quizBody.innerHTML = `
    <p>${question.prompt}</p>
    <div class="quiz-options">
      ${question.options
        .map(
          (option) => `
            <button class="quiz-option" data-option="${option}" type="button">${option}</button>
          `,
        )
        .join("")}
    </div>
    <button class="primary-action" id="submitAnswer" type="button" disabled>
      Submit answer
    </button>
  `;

  document.querySelectorAll(".quiz-option").forEach((button) => {
    button.addEventListener("click", () => {
      state.quiz.selected = button.dataset.option;
      document.querySelectorAll(".quiz-option").forEach((item) => item.classList.remove("selected"));
      button.classList.add("selected");
      document.getElementById("submitAnswer").disabled = false;
    });
  });

  document.getElementById("submitAnswer").addEventListener("click", submitAnswer);
}

function submitAnswer() {
  const question = questions[state.quiz.index];
  const correct = state.quiz.selected === question.answer;
  if (correct) {
    state.quiz.score += 1;
  }

  quizBody.innerHTML = `
    <div class="quiz-result">
      <strong>${correct ? "Correct" : "Not quite"}</strong>
      <p>${question.explanation}</p>
    </div>
    <button class="primary-action" id="nextQuestion" type="button">
      ${state.quiz.index === questions.length - 1 ? "Finish test" : "Next question"}
    </button>
  `;

  document.getElementById("nextQuestion").addEventListener("click", () => {
    if (state.quiz.index === questions.length - 1) {
      finishQuiz();
    } else {
      state.quiz.index += 1;
      state.quiz.selected = null;
      renderQuizQuestion();
    }
  });
}

function finishQuiz() {
  const percent = Math.round((state.quiz.score / questions.length) * 100);
  const xpGain = 80 + state.quiz.score * 40;
  state.xp += xpGain;
  state.streak += 1;

  leaders = leaders.map((student) =>
    student.current
      ? {
          ...student,
          xp: state.xp,
          score: Math.max(student.score, percent),
          tier: state.xp >= 3000 ? "Platinum" : student.tier,
        }
      : student,
  );

  const position = getSortedLeaders().findIndex((student) => student.current) + 1;
  state.rank = position;

  quizBody.innerHTML = `
    <div class="quiz-result">
      <strong>${percent}% score - ${xpGain} XP earned</strong>
      <p>
        Your leaderboard position is now ${position}. The recommendation engine will use this result
        to update your next study task.
      </p>
    </div>
    <button class="primary-action" id="finishClose" type="button">Back to dashboard</button>
  `;

  document.getElementById("finishClose").addEventListener("click", () => {
    closeQuiz();
    setView("dashboard");
  });
  renderCurrentView();
}

function addChatMessage(kind, text) {
  const chatLog = document.getElementById("chatLog");
  const node = document.createElement("div");
  node.className = `message ${kind}`;
  node.textContent = text;
  chatLog.appendChild(node);
  chatLog.scrollTop = chatLog.scrollHeight;
}

document.getElementById("navList").addEventListener("click", (event) => {
  const button = event.target.closest(".nav-item");
  if (button) {
    setView(button.dataset.view);
  }
});

document.querySelectorAll("[data-jump]").forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.jump));
});

document.querySelectorAll(".term-tab").forEach((button) => {
  button.addEventListener("click", () => {
    state.term = button.dataset.term;
    renderSubjects();
  });
});

document.querySelectorAll(".segment").forEach((button) => {
  button.addEventListener("click", () => {
    state.boardMode = button.dataset.board;
    renderLeaderboard();
  });
});

subjectFilter.addEventListener("change", () => {
  state.subject = subjectFilter.value;
  state.term = "Term 1";
  renderCurrentView();
});

document.getElementById("heroStartQuiz").addEventListener("click", () => openQuiz("Fractions"));
document.getElementById("closeQuiz").addEventListener("click", closeQuiz);

document.getElementById("chatForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.getElementById("chatInput");
  const value = input.value.trim();
  if (!value) return;
  addChatMessage("user", value);
  input.value = "";
  addChatMessage(
    "bot",
    `For ${state.subject}, start with the rule, then try one small example. Based on your scores, I would connect this question to your next weak topic practice.`,
  );
});

document.querySelectorAll(".prompt-chip").forEach((button) => {
  button.addEventListener("click", () => {
    document.getElementById("chatInput").value = button.textContent;
    document.getElementById("chatInput").focus();
  });
});

quizModal.addEventListener("click", (event) => {
  if (event.target === quizModal) {
    closeQuiz();
  }
});

renderCurrentView();
