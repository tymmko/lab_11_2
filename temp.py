def demo_bst(self, path: str):
        """Demonstration of efficiency binary search tree for the search
        tasks."""

        def get_info(path: str):
            with open(path) as file:
                all_lines = file.read().splitlines()
            return all_lines

        all_info = get_info(path)  # our info is list with all file words

        def get_random_words(info: list):
            """Retuns a list with 10 000 random words from a file."""
            result = []
            for _ in range(10000):
                result.append(random.choice(info))
            return result

        def sorted_words(info: list):
            """Retuns a list with 10 000 alphabet sorted words from a list
            with words."""
            result = list()
            for ind in range(10000):
                result.append(info[ind])
            return result

        def find_random_words(all_info: list):
            """Retuns time for searching 10 000 random words from a list with
            words."""
            rand_words = get_random_words(all_info)
            start_time = time()

            for word in rand_words:
                word in rand_words

            finish_time = time() - start_time
            print(f'Search time for random words in list: \
{format(finish_time, ".5f")} sec')

        def random_tree_find(all_info: list):
            """Retuns time for searching 10 000 random words in a BST."""
            tree = LinkedBST()
            rand_words = get_random_words(all_info)
            for word in rand_words:
                tree.add(word)

            start_time = time()

            for word in rand_words:
                tree.find(word)

            finish_time = time() - start_time
            print(f'Search time for random words in BST: \
{format(finish_time, ".5f")} sec')

        def balanced_random_tree_find(all_info: list):
            """Retuns time for searching 10 000 random words in a balanced
            BST."""
            tree = LinkedBST()
            rand_words = get_random_words(all_info)
            for word in rand_words:
                tree.add(word)

            tree.rebalance()
            start_time = time()

            for word in rand_words:
                tree.find(word)

            finish_time = time() - start_time
            print(f'Search time for random words in balanced BST: \
{format(finish_time, ".5f")} sec')

        def create_alphabet_tree(all_info: list):
            """Retuns time for searching 10 000 alphabet sorted words
            in a BST."""
            tree = LinkedBST()
            sort_words = sorted_words(all_info)
            for word in sort_words:
                tree.add(word)

            start_time = time()

            for word in sort_words:
                tree.find(word)

            finish_time = time() - start_time
            print(f'Search time for alphabet sorted words in BST: \
{format(finish_time, ".5f")} sec')

        # function calling
        find_random_words(all_info)
        random_tree_find(all_info)
        balanced_random_tree_find(all_info)
        create_alphabet_tree(all_info)