# Scholars League Product Brief

## Product Definition

Scholars League is an AI-powered academic platform where K-12 students learn, get tested automatically, and are ranked within their class. The platform starts with Nigeria's curriculum and is designed for later expansion into Ghana, Kenya, the UK, the US, and custom private-school curricula.

## Target Users

- Primary and secondary school students who want structured study and competition.
- Parents who want visible progress and motivation.
- Schools that want curriculum-aligned assessments and class rankings.
- Teachers or administrators who may later manage classes, invite codes, and reports.

## Student Experience

1. Sign up or log in.
2. Select country, grade, school, and class.
3. Load the correct curriculum module.
4. See today's tasks on the dashboard.
5. Study a topic from a subject hub.
6. Ask the AI tutor for help.
7. Take quizzes or tests.
8. Receive instant marking, feedback, XP, badge progress, and rank updates.
9. Follow personalized recommendations for weak topics.

## AI Features

| Feature | Purpose | MVP Version |
| --- | --- | --- |
| AI Tutor | Explains topics and answers subject questions conversationally. | Subject-scoped chat with curriculum context. |
| Auto Question Generation | Creates fresh topic-aligned questions so tests do not repeat. | Generate question drafts, then store reviewed questions. |
| Personalized Study Path | Detects weak topics and recommends what to study next. | Recommend topics based on low scores and incomplete work. |
| Performance Prediction | Forecasts likely end-of-term ranking. | Simple trend model based on recent scores and activity. |
| Adaptive Testing | Adjusts question difficulty in real time. | Difficulty step-up or step-down after answer streaks. |

## Gamification

- XP points for studying, passing tests, daily streaks, and challenges.
- Tiers: Bronze, Silver, Gold, Platinum, Scholar Elite.
- Leaderboards by subject and overall class rank.
- Badges such as Maths Wizard, 5-Day Streak, Most Improved, and Challenge Winner.
- Seasonal resets each term.
- Weekly subject challenges with XP boosts.

## Nigeria Curriculum Model

The Nigeria launch module should represent:

- Primary 1-6: Mathematics, English, Basic Science, Social Studies, Civic Education, and related subjects.
- JSS 1-3: English, Mathematics, Basic Science, Basic Technology, Social Studies, French, and related subjects.
- SS 1-3: Science, Commercial, and Arts tracks with track-specific subjects.
- Terms 1, 2, and 3 for every class.
- Topic-level tagging for lessons, quizzes, tests, scores, and mastery.

## Multi-Country Architecture

Each country should be implemented as a curriculum module:

- Country metadata.
- Grade/class naming.
- Term or semester structure.
- Subjects by grade and track.
- Topics by subject and term.
- Assessment rules.
- Optional localization rules.

Suggested launch order:

1. Nigeria
2. Ghana
3. Kenya
4. UK
5. US

Private and international schools should support custom curriculum modules later.

## Key Screens

### Home Dashboard

- Today's study tasks.
- Current class rank.
- XP progress bar.
- Streak count.
- Recommended next topic.
- Upcoming challenge.

### Subject Hub

- Subject overview.
- Term tabs.
- Topic list with completion status.
- Topic scores and mastery level.
- Practice and test actions.

### AI Tutor Chat

- Subject-aware chat.
- Topic context.
- Explanation modes such as simple, exam-style, and step-by-step.
- Suggested follow-up questions.

### Leaderboard

- Overall class ranking.
- Subject-specific ranking.
- XP, badges, and tier indicators.
- Weekly challenge ranking.

### Performance Insights

- Progress over time.
- Strong and weak topics.
- AI prediction card.
- Recommended recovery plan.

### Challenges Arena

- Active weekly challenges.
- Entry requirements.
- Time limits.
- Rewards.
- Class winners.

## Proposed System Architecture

### Frontend

- Web app dashboard.
- Subject hub.
- AI tutor chat.
- Leaderboards.
- Insights and challenge views.

### Backend API

- Authentication service.
- Curriculum service.
- Assessment service.
- Ranking engine.
- Gamification service.
- AI orchestration service.

### Data and AI Layer

- PostgreSQL for users, schools, classes, curriculum, scores, questions, and sessions.
- Redis for live leaderboard caches and streak counters.
- Object storage for content media.
- LLM service for tutoring, question generation, explanations, and insights.
- Adaptive testing engine for difficulty scaling.
- Prediction model for rank and performance forecasts.

## Suggested Data Entities

- User
- StudentProfile
- School
- ClassGroup
- Country
- Curriculum
- Grade
- Track
- Subject
- Term
- Topic
- Lesson
- Question
- Assessment
- AssessmentAttempt
- Score
- XPTransaction
- Badge
- StudentBadge
- LeaderboardSnapshot
- Challenge
- ChallengeAttempt
- TutorSession

## Important Product Decisions

### Class Formation

Recommended MVP: school code plus class invite code.

Students can join a school, then enter a class code provided by a teacher, school admin, or class creator. This is cleaner than letting students self-select arbitrary classes, because rankings are only meaningful when the class membership is trusted.

### Anti-Cheating

Recommended MVP controls:

- Randomized question pools.
- Time limits.
- Attempt limits.
- Question order shuffling.
- Suspicious pattern flags for unusually fast answers, repeated perfect scores, or device switching.
- Separate practice scores from ranked test scores.

### Content Strategy

Recommended MVP: combine human-authored curriculum maps with AI-assisted study notes and question drafts.

The curriculum map should be controlled and reviewed. AI can help generate explanations, practice variations, and question drafts, but ranked assessments should use approved or reviewed questions first.

### Monetization

Recommended MVP:

- Free student tier with curriculum access, quizzes, leaderboards, and limited AI tutor use.
- Premium tier with deeper tutor access, personalized plans, advanced insights, and extra practice packs.
- Future school plan for class management, reporting, and custom curriculum.

## MVP Build Order

1. Create app shell and visual system.
2. Implement onboarding for country, grade, school, and class.
3. Add Nigeria curriculum seed data.
4. Build dashboard, subject hub, quiz flow, and results view.
5. Add XP, streaks, tiers, and leaderboard calculations.
6. Add AI tutor integration or placeholder flow.
7. Add performance insights and recommendations.
8. Add challenges arena.

## First Prototype Goal

Build a working web prototype with seeded demo data for a Nigerian JSS 1 student. The prototype should demonstrate:

- A dashboard with rank, XP, streak, tasks, and recommendations.
- A subject hub with term topics.
- A quiz/test flow with auto-marking.
- Leaderboard updates after a completed test.
- A tutor chat interface.
- Basic performance insights.
