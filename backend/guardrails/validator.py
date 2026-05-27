def validate_question(question: str) -> bool:
    """
    Validate the user's question.
    Returns True if the question is valid, False otherwise.
    """
    if not question:
        return False
        
    stripped = question.strip()
    if len(stripped) < 3:
        return False
        
    # Basic guardrail check to prevent empty/nonsense inputs
    return True
