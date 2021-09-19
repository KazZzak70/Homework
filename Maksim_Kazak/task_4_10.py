def generate_squares(number: int = None) -> dict[int]:
    if number is not None and number > 0:
        output_dict = dict()
        for index in range(number):
            output_dict[index + 1] = (index + 1) ** 2
        return output_dict


if __name__ == "__main__":
    example = 5
    print(f"Example: {example}\nOutput: {generate_squares(example)}")
