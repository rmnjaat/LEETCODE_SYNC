"""
Configuration settings loader
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

from src.utils.logger import get_logger

logger = get_logger(__name__)


class Settings:
    """Application settings"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Load settings from config file and environment
        
        Args:
            config_path: Path to config YAML file
        """
        # Load environment variables
        load_dotenv()
        
        # Load config file
        self.config = self._load_config(config_path)
        
        # Load tag mappings
        self.tag_mappings = self._load_tag_mappings()
        
        # Environment variables (secrets)
        self.leetcode_session = os.getenv("LEETCODE_SESSION", "")
        self.leetcode_csrf = os.getenv("LEETCODE_CSRF_TOKEN", "")
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        
        # Validate
        self._validate()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load config from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"✓ Loaded configuration from {config_path}")
                return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return self._get_default_config()
    
    def _load_tag_mappings(self) -> Dict:
        """Load tag mappings from YAML file"""
        try:
            with open("config/tag_mappings.yaml", 'r') as f:
                mappings = yaml.safe_load(f)
                logger.info("✓ Loaded tag mappings")
                return mappings
        except FileNotFoundError:
            logger.warning("Tag mappings file not found, using defaults")
            return self._get_default_tag_mappings()
        except Exception as e:
            logger.error(f"Error loading tag mappings: {str(e)}")
            return self._get_default_tag_mappings()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "leetcode": {
                "username": "",
                "base_url": "https://leetcode.com",
                "api_endpoint": "https://leetcode.com/graphql"
            },
            "github": {
                "username": "",
                "repository": "leetcode-solutions",
                "branch": "main"
            },
            "sync_settings": {
                "days_to_look_back": 30,
                "only_accepted": True,
                "keep_all_versions": True,
                "version_naming": "sequential"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/sync.log"
            }
        }
    
    def _get_default_tag_mappings(self) -> Dict:
        """Get default tag mappings"""
        return {
            "tag_mappings": {
                "Database": "Databases"
            },
            "active_tags": ["Database"]
        }
    
    def _validate(self):
        """Validate required settings"""
        errors = []
        
        if not self.leetcode_session:
            errors.append("LEETCODE_SESSION not set in .env")
        
        if not self.github_token:
            errors.append("GITHUB_TOKEN not set in .env")
        
        if not self.leetcode_username:
            errors.append("LeetCode username not set in config")
        
        if not self.github_username:
            errors.append("GitHub username not set in config")
        
        if errors:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            # Don't raise exception, allow user to proceed and fix
    
    # Properties for easy access
    @property
    def leetcode_username(self) -> str:
        return self.config.get("leetcode", {}).get("username", "")
    
    @property
    def github_username(self) -> str:
        return self.config.get("github", {}).get("username", "")
    
    @property
    def github_repository(self) -> str:
        return self.config.get("github", {}).get("repository", "leetcode-solutions")
    
    @property
    def github_branch(self) -> str:
        return self.config.get("github", {}).get("branch", "main")
    
    @property
    def days_to_look_back(self) -> int:
        return self.config.get("sync_settings", {}).get("days_to_look_back", 30)
    
    @property
    def only_accepted(self) -> bool:
        return self.config.get("sync_settings", {}).get("only_accepted", True)
    
    @property
    def keep_all_versions(self) -> bool:
        return self.config.get("sync_settings", {}).get("keep_all_versions", True)
    
    @property
    def active_tags(self) -> List[str]:
        return self.tag_mappings.get("active_tags", ["Database"])
    
    @property
    def tag_folder_mappings(self) -> Dict[str, str]:
        return self.tag_mappings.get("tag_mappings", {"Database": "Databases"})
    
    @property
    def log_level(self) -> str:
        return self.config.get("logging", {}).get("level", "INFO")
    
    @property
    def log_file(self) -> str:
        return self.config.get("logging", {}).get("file", "logs/sync.log")
