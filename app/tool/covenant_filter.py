"""
NATIONOS COVENANT FILTER MODULE

This module implements covenant-based filtering for browser and web access tools.
It ensures that all web interactions align with the sanctified purpose of the agent.

Biblical Foundation:
"Finally, brethren, whatever is true, whatever is honorable, whatever is right,
whatever is pure, whatever is lovely, whatever is of good repute, if there is
any excellence and if anything worthy of praise, dwell on these things."
— Philippians 4:8
"""

import re
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from app.logger import logger


class CovenantFilter:
    """Covenant-based URL and content filter for sanctified web access."""
    
    # Blacklist: Known degenerate or hostile domains
    BLACKLIST_DOMAINS = [
        # Pornography and adult content
        r".*porn.*",
        r".*xxx.*",
        r".*adult.*",
        # Gambling
        r".*casino.*",
        r".*betting.*",
        # Occult and explicitly satanic content
        r".*occult.*",
        r".*satanic.*",
        # Add more patterns as needed
    ]
    
    # Whitelist: Explicitly approved covenant-aligned domains
    WHITELIST_DOMAINS = [
        r"github\.com",
        r"libertythroughtruth\.org",
        r".*\.libertythroughtruth\.org",
        r"pulsechain\.com",
        r"bible\.com",
        r"biblegateway\.com",
        r"logos\.com",
        # Add more approved domains as needed
    ]
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the covenant filter.
        
        Args:
            strict_mode: If True, only whitelisted domains are allowed.
                        If False, all domains except blacklisted are allowed.
        """
        self.strict_mode = strict_mode
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns for efficient matching."""
        self.blacklist_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.BLACKLIST_DOMAINS
        ]
        self.whitelist_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.WHITELIST_DOMAINS
        ]
    
    def is_url_sanctified(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a URL is sanctified (approved for access).
        
        Args:
            url: The URL to check
            
        Returns:
            Tuple of (is_sanctified, reason)
            - is_sanctified: True if URL is approved, False otherwise
            - reason: Explanation for the decision
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check whitelist first
            for pattern in self.whitelist_patterns:
                if pattern.match(domain):
                    logger.info(f"[COVENANT FILTER] URL approved (whitelisted): {url}")
                    return True, "Domain is explicitly whitelisted"
            
            # Check blacklist
            for pattern in self.blacklist_patterns:
                if pattern.match(domain):
                    logger.warning(f"[COVENANT FILTER] URL blocked (blacklisted): {url}")
                    return False, "Domain matches blacklist pattern (degenerate content)"
            
            # In strict mode, reject anything not whitelisted
            if self.strict_mode:
                logger.warning(f"[COVENANT FILTER] URL blocked (strict mode): {url}")
                return False, "Strict mode enabled: only whitelisted domains allowed"
            
            # Default: allow if not blacklisted
            logger.info(f"[COVENANT FILTER] URL approved (not blacklisted): {url}")
            return True, "Domain not blacklisted"
            
        except Exception as e:
            logger.error(f"[COVENANT FILTER] Error parsing URL {url}: {e}")
            return False, f"URL parsing error: {e}"
    
    def filter_url_list(self, urls: List[str]) -> List[str]:
        """
        Filter a list of URLs, returning only sanctified ones.
        
        Args:
            urls: List of URLs to filter
            
        Returns:
            List of sanctified URLs
        """
        sanctified_urls = []
        for url in urls:
            is_sanctified, reason = self.is_url_sanctified(url)
            if is_sanctified:
                sanctified_urls.append(url)
        
        return sanctified_urls
    
    @classmethod
    def add_to_whitelist(cls, domain_pattern: str) -> None:
        """
        Add a domain pattern to the whitelist.
        
        Args:
            domain_pattern: Regex pattern for the domain to whitelist
        """
        if domain_pattern not in cls.WHITELIST_DOMAINS:
            cls.WHITELIST_DOMAINS.append(domain_pattern)
            logger.info(f"[COVENANT FILTER] Added to whitelist: {domain_pattern}")
    
    @classmethod
    def add_to_blacklist(cls, domain_pattern: str) -> None:
        """
        Add a domain pattern to the blacklist.
        
        Args:
            domain_pattern: Regex pattern for the domain to blacklist
        """
        if domain_pattern not in cls.BLACKLIST_DOMAINS:
            cls.BLACKLIST_DOMAINS.append(domain_pattern)
            logger.info(f"[COVENANT FILTER] Added to blacklist: {domain_pattern}")


# Global covenant filter instance
_covenant_filter: Optional[CovenantFilter] = None


def get_covenant_filter(strict_mode: bool = False) -> CovenantFilter:
    """
    Get the global covenant filter instance.
    
    Args:
        strict_mode: Enable strict whitelist-only mode
        
    Returns:
        CovenantFilter instance
    """
    global _covenant_filter
    if _covenant_filter is None:
        _covenant_filter = CovenantFilter(strict_mode=strict_mode)
    return _covenant_filter


def sanctify_url(url: str, strict_mode: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Convenience function to check if a URL is sanctified.
    
    Args:
        url: The URL to check
        strict_mode: Enable strict whitelist-only mode
        
    Returns:
        Tuple of (is_sanctified, reason)
    """
    filter_instance = get_covenant_filter(strict_mode=strict_mode)
    return filter_instance.is_url_sanctified(url)
