import os

# Token cost in dollars
token_cost = 0.0080  # $0.0080 per 1K tokens

def count_tokens(file_path):
    """
    Count the number of tokens in a given file.

    Args:
    - file_path (str): Path to the input file.

    Returns:
    - int: Number of tokens in the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # Splitting by space for a simple tokenization (this can be improved based on the specific use case)
        tokens = text.split()
        return len(tokens)

def estimate_cost(file_path):
    """
    Estimate the cost for fine-tuning a model based on the number of tokens in the input file.

    Args:
    - file_path (str): Path to the input file.

    Returns:
    - float: Estimated cost in dollars.
    """
    num_tokens = count_tokens(file_path)
    print(num_tokens)
    cost = (num_tokens / 1000) * token_cost
    return cost

def main():
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Assuming the file is in the same directory as the script
    file_name = input("Enter the name of the input file: ")
    file_path = os.path.join(script_dir, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        print("File not found. Please make sure the file is in the same directory as the script.")
        return

    # Estimate the cost and display the result
    estimated_cost = estimate_cost(file_path)
    print(f"\nEstimated cost for fine-tuning: ${estimated_cost:.2f}")

if __name__ == "__main__":
    main()
