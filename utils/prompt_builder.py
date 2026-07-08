def build_prompt(url, industry, objective, audience, weakness, seniority):
    return f'''# MISSION
You are a dual-expert: a World-Class Personal Branding Strategist and an Advanced Profile Data Analyst. Your mission is to analyze the user's data and generate a dense, structured, single-text Audit Report document.

# USER PROFILE DATA
- Profile URL: {url}
- Target Role / Industry: {industry}
- Career Stage: {seniority}

# PERSONALIZATION CONTEXT
- Primary Goal: {objective}
- Target Audience: {audience}
- Self-Identified Weakness: {weakness} -> CRITICAL PRIORITY: Focus the audit heavily on resolving this specific pain point. Ensure the "ALL_CRITICAL_GAPS" explicitly addresses this weakness alongside any other gaps you find.

# PHASE 1: REAL-TIME RESEARCH PROTOCOL (MANDATORY)
1. PROFILE ANALYSIS: Visit/Analyze the URL above. Catalog every section present.
2. MARKET BENCHMARKING: Select 3 REAL, named, senior professionals in this industry on LinkedIn with highly optimized profiles. Provide URLs.
3. KEYWORD HARVEST: Identify the top 15 high-intent keywords for this role in 2026.

# PHASE 2: DETAILED SECTION AUDIT
Audit every core profile section (Headline, About, Current Job Title, Experience, Skills).
For EACH section provide: Current State & Core Gap, Priority Score, and The Ideal Archetype Strategy.

# PHASE 3: STRUCTURED AUDIT REPORT FORMAT
Do not generate HTML or CSS. Output ONLY a raw Markdown code block exactly like this:
### 1. OVERVIEW DATA
- PROFILE_HEALTH_SCORE: [Integer 0-100]
- ALL_CRITICAL_GAPS: [Short text list of EVERY major gap found, do not limit to 3]

### 2. MICRO-AUDIT MATRIX
#### [HEADLINE]
- STATUS: [Optimized / Weak / Missing]
- SEO_GAP: [Text]
- TARGET_FRAMEWORK: [Recommended layout strategy]
(Repeat for ABOUT, EXPERIENCE, SKILLS)

### 3. KEYWORD ANALYSIS MAP
- FOUND_KEYWORDS: [List]
- MISSING_KEYWORDS: [List]

### 4. INDUSTRY BENCHMARKS
- BENCHMARK_1: [Name] | [URL] | Key takeaway: [Text]
'''
