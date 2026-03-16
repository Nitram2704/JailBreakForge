"""Seed template loader for JailbreakForge."""

from __future__ import annotations

import importlib.resources
from dataclasses import dataclass

import yaml


@dataclass
class SeedTemplate:
    """A single jailbreak seed template loaded from YAML."""
    
    category: str
    name: str
    prompt: str
    mutation_hints: list[str]


def list_categories() -> list[str]:
    """Return a list of all available attack categories."""
    categories = []
    # Use importlib.resources to find yaml files in the seeds package
    try:
        from jailbreakforge import seeds as seeds_pkg
        for filepath in importlib.resources.files(seeds_pkg).iterdir():
            if filepath.suffix in (".yaml", ".yml"):
                categories.append(filepath.stem)
    except ModuleNotFoundError:
        pass
    
    return sorted(categories)


def load_seeds(categories: list[str] | None = None) -> dict[str, list[SeedTemplate]]:
    """Load seed templates from YAML files.

    Args:
        categories: Optional list of category names to load. If None, loads all.

    Returns:
        Dictionary mapping category name to list of SeedTemplates.
    """
    from jailbreakforge import seeds as seeds_pkg
    
    result: dict[str, list[SeedTemplate]] = {}
    
    for filepath in importlib.resources.files(seeds_pkg).iterdir():
        if filepath.suffix not in (".yaml", ".yml"):
            continue
            
        category_name = filepath.stem
        if categories is not None and category_name not in categories:
            continue
            
        content = filepath.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        
        if not data or "seeds" not in data:
            continue
            
        templates = []
        for seed_data in data["seeds"]:
            templates.append(
                SeedTemplate(
                    category=category_name,
                    name=seed_data["name"],
                    prompt=seed_data["prompt"],
                    mutation_hints=seed_data.get("mutation_hints", []),
                )
            )
            
        if templates:
            result[category_name] = templates
            
    return result
