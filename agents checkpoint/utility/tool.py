from langchain_core.tools import tool
import math
from .search_utility import search,scrape

@tool
def calculator(numbers: list[float], operation: str) -> float:
    """
    Perform an arithmetic operation on a list of numbers.

    Use this tool whenever the user needs a mathematical calculation,
    such as addition, subtraction, multiplication, division, or a
    square root.

    Args:
        numbers (list[float]): The numbers to operate on, in order.
            - For "add", "subtract", "multiply", "divide": provide two
              or more numbers. Operations are applied left to right
              (e.g. subtract on [10, 2, 3] returns 10 - 2 - 3).
            - For "sqrt": provide exactly one non-negative number.
        operation (str): One of "add", "subtract", "multiply",
            "divide", "sqrt".

    Returns:
        float: The result of applying the operation to the numbers.

    Raises:
        ValueError: If operation is unknown, if "sqrt" is given more
            or less than one number, or if "sqrt" is given a negative
            number.
        ZeroDivisionError: If "divide" is used and any number after
            the first is 0.

    Example:
        calculator([4, 2], "add") -> 6
        calculator([10, 5], "divide") -> 2.0
        calculator([144], "sqrt") -> 12.0
    """
    if operation == "add":
        return sum(numbers)
    if operation == "subtract":
        res = numbers[0]
        for n in numbers[1:]:
            res -= n
        return res
    if operation == "multiply":
        prod = 1
        for n in numbers:
            prod *= n
        return prod
    if operation == "divide":
        if 0 in numbers[1:]:
            raise ZeroDivisionError("You can't divide by 0")
        res = numbers[0]
        for n in numbers[1:]:
            res /= n
        return res
    if operation == "sqrt":
        if len(numbers) != 1:
            raise ValueError("sqrt takes exactly 1 number")
        if numbers[0] < 0:
            raise ValueError("sqrt doesn't accept negative values")
        return math.sqrt(numbers[0])
    raise ValueError(f"Unknown operation: {operation}")

@tool
def google_search(query: str) -> str:
    """
    Search the web for a query and return cleaned text content from the
    top results.

    Use this tool when the user asks about current events, facts you
    don't know, or anything requiring up-to-date information from the
    internet.

    Args:
        query (str): The search query, in natural language.

    Returns:
        str: Concatenated, cleaned text scraped from the top search
            results, separated by "## RESULT" markers. Only results
            with more than 250 characters of content are included.

    Raises:
        RuntimeError: If the search request fails, times out, or
            returns no usable results.

    Example:
        google_search("current population of Tunisia")
    """
    search_result = search(query)

    if not isinstance(search_result, list):
        raise RuntimeError(f"Search failed: {search_result}")

    text = []
    for result in search_result:
        link = result.get("link")
        if not link:
            continue
        try:
            text.append(f"## RESULT\n{scrape(link)}")
        except Exception as e:
            continue 

    text = [x for x in text if len(x) > 250]

    if not text:
        raise RuntimeError("No usable search results found")

    return "\n".join(text)



