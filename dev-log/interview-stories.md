# HabitOS Interview Stories

This is a source doc for resume writing and interview prep. Each story below has:
- A one-line resume framing at the top
- A 4-7 sentence story for interview use
- Notes on which questions this story answers best

Last updated: July 18, 2026

---

## Story 1: Secure JWT Authentication

**Resume framing:**
Built secure JWT authentication with FastAPI and python-jose. Prevented email enumeration by returning identical errors for missing users and wrong passwords. Returned 404 (not 403) for cross-user resource access to prevent existence leaks. Passed explicit algorithm allowlist to jwt.decode() to block algorithm-substitution attacks.

**Interview story:**

For added security, my auth endpoint returns "invalid credentials" regardless of whether the email is not registered or the password is incorrect. This protects users from hackers figuring out which emails are registered. Across users, the 404 status code is used instead of the 403 status code so if a user attempts to access another user's habits, it doesn't leak any information. On the JWT side, I explicitly pass an allowlist of accepted algorithms to jwt.decode(). Without this, an attacker could craft a token claiming to use no algorithm (alg: none) and my code would accept it as valid — a real attack class called algorithm substitution.

**Best for questions like:**
- "Tell me about a technical decision you're proud of"
- "What's a security consideration you had to think about"
- "Walk me through your auth flow"

---

## Story 2: Backend Architecture (Habit History Endpoint)

**Resume framing:**
Designed a time-series REST endpoint for habit completion history in FastAPI. Established a layered pattern where domain-specific exceptions raised in the service layer are translated to HTTP status codes in the router layer. Enforced user ownership through parent-resource verification rather than redundant child filters, reflecting deliberate domain modeling.

**Interview story:**

When I created the get_habit_history service, I initially used the wrong service template. I copied the shape of list_habits_with_status when the closest pattern was list_completions so I could list the completions on to a heatmap. Recognizing this mix up while implementing allowed me to switch to the right pattern with ease. I also realized I didn't need a user_id parameter on the completions query because I already verified the parent habit belongs to the user. This was cleaner and prevented me from introducing potential user_id bugs. The endpoint uses a layered pattern so schemas create the structure of the data, services raise exceptions, and routers translate the exceptions to HTTP status codes.

**Best for questions like:**
- "Walk me through a technical challenge"
- "How do you approach system design"
- "Tell me about a bug you found and fixed"

---

## Story 3: Frontend Redesign as Intentional Design

**Resume framing:**
Redesigned frontend from generic dark-theme to a warm, palette-driven visual identity extracted from personal film photography. Built a design system in CSS custom properties covering color scales, spacing, and typography. Chose single-family Nunito over a heading/body pair to let the palette carry visual personality, and restricted decorative animation (react-wavify) to entry pages for intentionality.

**Interview story:**
Originally, HabitOS featured a dark purple theme that didn't match the warmth I wanted for a habit tracker. I redesigned HabitOS by picking colors from photos I had taken myself. I used ocean blues from lakes and sunset yellows from clouds in the sky. The design system uses CSS custom properties from the color scale, spacing scale, and typography so changing a color is done by editing one variable. I used the Nunito font to soften the letters and restricted the wave to the entry pages to avoid overcrowding the main dashboard. This project let me bring my 4 years of photography and drawing experience into the UI.

**Best for questions like:**
- "What makes you different from other candidates"
- "Tell me about your visual/design sensibility"
- "What are you proud of in this project"
- Especially strong for health tech companies with patient-facing tools (Flatiron, Tempus)

---

## Notes for August resume writing

When drafting resume bullets:
- Start with the resume framing above as v1
- Cut anything that reads as "I did X" without a "why" or a "result"
- Aim for one bullet per story on the resume, not three
- Save the full stories for interviews, cover letters, and Behavioral rounds

## Which story to lead with

- **Technical depth questions:** Auth (most specific, most impressed a working engineer)
- **Design/personality questions:** Redesign (unique combination)
- **Systems/architecture questions:** Backend history endpoint (best judgment story)