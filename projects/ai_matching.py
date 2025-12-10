# projects/ai_matching.py
"""
AI Matching Engine - Stub minimal
Funzionalità completa da implementare
"""
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class TalentMatcher:
    """
    AI Talent Matcher - Versione stub
    TODO: Implementare logica di matching completa
    """
    
    def __init__(self):
        """Inizializza il matcher"""
        logger.info("TalentMatcher initialized (stub version)")
    
    def find_candidates(self, project, max_results=10):
        """
        Trova candidati per un progetto
        
        Args:
            project: Oggetto Project
            max_results: Numero massimo di risultati
            
        Returns:
            Lista vuota (stub)
        """
        logger.warning("TalentMatcher.find_candidates() called but not implemented")
        return []
    
    def match_users_to_project(self, project_id, limit=20):
        """
        Match utenti a progetto per ID
        
        Args:
            project_id: ID del progetto
            limit: Limite risultati
            
        Returns:
            Lista vuota (stub)
        """
        logger.warning("TalentMatcher.match_users_to_project() called but not implemented")
        return []
    
    def calculate_match_score(self, user, project):
        """
        Calcola score di matching
        
        Args:
            user: Oggetto User
            project: Oggetto Project
            
        Returns:
            0.0 (stub)
        """
        return 0.0
    
    def get_top_matches(self, project, users, top_n=10):
        """
        Ottieni top N matches
        
        Args:
            project: Oggetto Project
            users: QuerySet di User
            top_n: Numero di top match
            
        Returns:
            Lista vuota (stub)
        """
        logger.warning("TalentMatcher.get_top_matches() called but not implemented")
        return []


def run_matching_algorithm(project_id: int, preferences: Dict = None) -> List:
    """
    Funzione standalone per matching
    
    Args:
        project_id: ID del progetto
        preferences: Preferenze di matching (opzionale)
        
    Returns:
        Lista vuota (stub)
    """
    logger.warning(f"run_matching_algorithm() called for project {project_id} but not implemented")
    return []
