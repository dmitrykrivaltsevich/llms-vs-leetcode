from collections import deque, defaultdict
from typing import List

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        # Convert supplies to a set for O(1) lookups
        supply_set = set(supplies)

        # Build the graph and in-degree count
        graph = defaultdict(list)
        in_degree = {recipe: 0 for recipe in recipes}

        # Add edges to the graph and calculate in-degrees
        for recipe, ingredient_list in zip(recipes, ingredients):
            can_make = True
            for ingredient in ingredient_list:
                if ingredient not in supply_set:
                    if ingredient in recipes:
                        graph[ingredient].append(recipe)
                        in_degree[recipe] += 1
                    else:
                        can_make = False
                        break
            if can_make and all(ing in supply_set for ing in ingredient_list):
                queue.append(recipe)

        # Initialize the queue with recipes that have no dependencies (in-degree 0)
        queue = deque([recipe for recipe in recipes if in_degree.get(recipe, 0) == 0])
        result = []

        # Process the queue
        while queue:
            current_recipe = queue.popleft()
            result.append(current_recipe)

            for neighbor in graph[current_recipe]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result
