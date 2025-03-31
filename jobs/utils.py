import re
import google.generativeai as genai
from django.conf import settings
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Simple list of potential technical skills keywords
# This list can be expanded significantly for better accuracy
SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'html', 'css', 'sql', 'nosql',
    'django', 'flask', 'spring', 'react', 'angular', 'vue', 'node.js', 'express',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'linux', 'unix',
    'machine learning', 'deep learning', 'nlp', 'natural language processing', 'data analysis',
    'data science', 'statistics', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
    'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'devops', 'ci/cd',
    'security', 'testing', 'automation', 'big data', 'hadoop', 'spark'
]

def extract_skills_from_description(description):
    """
    Extracts potential skills from a job description using keyword matching.
    This is a basic implementation and can be improved with more sophisticated NLP techniques.
    """
    if not description:
        return ""

    # Convert to lowercase and remove punctuation for simpler matching
    processed_description = re.sub(r'[^\w\s]', '', description.lower())
    
    found_skills = set()
    # Use word boundaries to avoid matching parts of words (e.g., 'java' in 'javascript')
    for skill in SKILL_KEYWORDS:
        # Handle multi-word skills and single-word skills
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, processed_description):
            found_skills.add(skill.strip()) # Use original casing/format if desired, or keep lowercase

    # Return skills as a comma-separated string
    return ", ".join(sorted(list(found_skills)))


def generate_interview_questions(job_role, skills):
    """
    Generates interview questions using the Gemini API based on job role and skills.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        logger.error("GEMINI_API_KEY not found in settings.")
        return "Error: Gemini API Key not configured."
    
    if not job_role or not skills:
        return "Error: Job role and skills must be provided."

    try:
        genai.configure(api_key=api_key)
        
        # For text-only input, use the gemini-pro model
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Generate 5-7 relevant interview questions for the job role '{job_role}'. 
        The candidate should possess the following skills: {skills}.
        Focus on questions that assess both technical proficiency in the listed skills 
        and how they apply to the specific job role. Include a mix of technical, 
        behavioral, and situational questions if appropriate for the role.
        
        Format the output as a numbered list.
        """

        response = model.generate_content(prompt)
        
        # Basic check if the response contains text
        if response.text:
            return response.text.strip()
        else:
            # Log the full response if text is missing (might indicate an issue)
            logger.warning(f"Gemini API returned response without text. Full response: {response}")
            # Check for safety ratings or other reasons for blocked content
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                 return f"Error: Content generation blocked. Reason: {response.prompt_feedback.block_reason}"
            return "Error: Could not generate questions. The API returned an empty response."

    except Exception as e:
        logger.error(f"Error generating interview questions using Gemini API: {e}", exc_info=True)
        return f"Error: An unexpected error occurred while generating questions: {e}"
