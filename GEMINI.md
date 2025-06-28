# Core Development Guidelines

This document outlines the essential principles and practices for development in this project. Adherence to these guidelines is crucial for maintaining code quality, ensuring collaboration is smooth, and delivering robust, maintainable software.

---

## 1. Core Philosophy

Our goal is not just to write code that works, but to write programs that are resilient, adaptable, and easy to understand. We prioritize clarity over cleverness and long-term maintainability over short-term gains. Every contribution should aim to leave the codebase in a better state than it was found.

## 2. The TDD Cycle: Red, Green, Refactor

All development must follow a strict Test-Driven Development (TDD) loop. This practice ensures that we have a comprehensive, automated test suite and that our code is designed with testability in mind from the start.

1.  **RED: Add a Test**
    * Before writing any implementation code, write a single failing test that defines a new function or an improvement.
    * The test should fail for the expected reason. This proves that the test is valid and that the feature doesn't already exist.

2.  **GREEN: Write Code to Pass**
    * Write the simplest, most straightforward code possible to make the test pass.
    * At this stage, do not worry about elegance or optimal design. The goal is solely to get the test to pass.

3.  **REFACTOR: Improve the Code**
    * With the safety net of passing tests, refactor the implementation code.
    * Focus on improving structure, removing duplication, increasing clarity, and enhancing performance.
    * Run the tests again to ensure that your refactoring has not broken any existing functionality. The tests must remain green.

## 3. Production Code: Structured Programming

Every function written for the production codebase (i.e., not test code) must adhere to the principles of structured programming. This means a clear, logical flow and a well-defined contract for every function.

### Function Pre-conditions and Post-conditions

Every function must be documented with explicit pre-conditions and post-conditions. This forms a "contract" that makes the function's behavior predictable and easier to reason about.

* **Pre-conditions**: What must be true *before* the function is called? This includes constraints on arguments (e.g., type, range, format), system state, and dependencies. The function is not guaranteed to work if its pre-conditions are not met.
* **Post-conditions**: What is guaranteed to be true *after* the function completes successfully? This describes the return value, side effects on the system, and changes to any objects passed by reference.

**Example (Python):**
```python
def calculate_discount(price: float, percentage: float) -> float:
    """
    Calculates the final price after applying a discount.

    :param price: The original price of the item.
                  Pre-condition: Must be a non-negative float.
    :param percentage: The discount percentage.
                       Pre-condition: Must be a float between 0.0 and 100.0.
    :return: The price after the discount is applied.
             Post-condition: The returned value is a non-negative float
                             and is less than or equal to the original price.
    """
    # Pre-condition checks (can be assertions or explicit checks)
    assert price >= 0, "Price cannot be negative."
    assert 0.0 <= percentage <= 100.0, "Percentage must be between 0 and 100."

    discount_amount = price * (percentage / 100)
    final_price = price - discount_amount

    # Post-condition check (optional, but good for complex logic)
    assert final_price >= 0
    assert final_price <= price

    return final_price
````

## 4. Formatting and Style

  * **Indentation**: Use four (4) spaces for each level of indentation. Do not use tabs.
  * **Line Length**: Aim for a maximum line length of 80-100 characters to ensure readability.
  * **Naming Conventions**: Use clear, descriptive, and consistent names for variables, functions, classes, and files. Follow the standard convention for the language being used (e.g., `snake_case` in Python, `camelCase` in JavaScript).

## 5. Composite Best Practices

The following practices are compiled from the perspectives of various roles in a software development team.

### Design & Architecture

  * **(Architect)** **Scalability First**: Design components with future scale in mind. Avoid premature optimization, but also avoid designs that are inherently difficult to scale.
  * **(Architect)** **Loose Coupling, High Cohesion**: Modules should be independent and focused on a single responsibility.
  * **(OO Programmer)** **SOLID Principles**: Adhere to the SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
  * **(Functional Programmer)** **Favor Pure Functions**: Where possible, use pure functions and immutable data structures to minimize side effects and make code easier to test and reason about.

### Code Quality & Readability

  * **(Developer)** **Clarity is King**: Write code that is easy for a new team member to understand. Avoid obscure language features or overly complex one-liners.
  * **(Code Reviewer)** **The Boy Scout Rule**: Leave the code cleaner than you found it.
  * **(CTO/Tech Lead)** **Manage Technical Debt**: Consciously manage and document any technical debt. Add tasks to TASKS.md file to address it in the future. Don't let it accumulate silently.

### Security & Reliability

  * **(Cybersecurity Specialist)** **Secure by Design**: Sanitize all inputs from external sources. Use parameterized queries to prevent SQL injection. Never trust client-side data.
  * **(Cybersecurity Specialist)** **Dependency Management**: Regularly scan and update dependencies to patch known vulnerabilities.
  * **(SRE)** **Embrace Observability**: Instrument your code with logging, metrics, and tracing. Ensure that you can understand the state of the system in production without needing to debug it live.
  * **(Compliance Officer)** **Data Privacy**: Be mindful of PII and other sensitive data. Ensure all data handling complies with relevant regulations (e.g., GDPR, HIPAA).

### Testing & Quality Assurance

  * **(QA Engineer)** **Test Beyond the "Happy Path"**: Your tests must cover edge cases, invalid inputs, and potential failure modes.
  * **(Performance Engineer)** **Benchmark Critical Paths**: For performance-sensitive code, write benchmarks in addition to correctness tests.

### Process & Collaboration

  * **(DevOps Engineer)** **Automate Everything**: Automate builds, tests, and deployments through a robust CI/CD pipeline. The process of shipping code should be reliable and repeatable.
  * **(Agile Coach)** **Small, Atomic Commits**: Keep commits small and focused on a single logical change. Write clear, descriptive commit messages. Use conventional commits format.
  * **(Product Manager)** **Align with Requirements**: Ensure your implementation directly maps to the specified requirements. If a requirement is unclear, ask for clarification before building.
  * **(Open Source Contributor)** **PR Etiquette**: Pull requests should be focused, well-described, and link to the relevant issue or ticket. Be receptive to feedback.

### Documentation

  * **(Technical Writer)** **Document the "Why"**: Your code explains *how* it works. Your comments and documentation should explain *why* it exists and the design decisions behind it.
  * **(UI/UX Designer)** **Document Design Decisions**: For front-end components, document the rationale behind UI/UX choices to maintain a consistent user experience.

### Data Management

  * **(DBA)** **Efficient Data Access**: Be mindful of database performance. Avoid N+1 query problems. Ensure proper indexing for common query patterns.
  * **(Data Scientist)** **Ensure Data Integrity**: Implement checks and constraints to maintain the quality and integrity of the data your application produces and consumes.

