import time


def typing_test(sentence):
    start_time = time.time()
    user_input = input("Type the following sentence: \n" + sentence + "\n")
    end_time = time.time()

    # Calculate typing speed
    time_elapsed = end_time - start_time
    words = len(sentence.split())
    typing_speed = round(words / (time_elapsed / 60),2)

    # Calculate accuracy
    accuracy = sum(sentence[i] == user_input[i] for i in range(len(sentence)))
    accuracy = round(accuracy / len(sentence) * 100, 2)

# Test the function with a sample text
text = "The quick brown fox jumps over the lazy dog."
typing_test(text)
