import pdb

DELIMITER = ', '

class OutlierFP:
    def mine(self, filepath, output_filepath):
        self.output_filepath = output_filepath
        self._read_file(filepath)
        k, itemsets = self._mine_frequent_itemsets()
        resilient_itemsets = self._find_epsilon_resilient_itemsets(k, itemsets)
        self._create_output(resilient_itemsets)

    def _read_file(self, filepath):
        self.sequences = []
        with open(filepath, 'r') as data_file:
            parameters = data_file.readline().split(DELIMITER)
            self.theta = float(parameters[ 0 ])
            self.epsilon = float(parameters[ 1 ])

            for line in data_file:
                self.sequences.append(line.replace('\n', '').split(DELIMITER))

            self.minsup = len(self.sequences) * self.theta

    """
    self.ranges holds the different ranges in which a pattern can be found on each
    transaction. It is represented as an array where the position is the length of
    the pattern and the value is in itself an array where each item corresponds to
    a sequence (a map of each pattern and the ranges)
    """
    def _mine_frequent_itemsets(self):
        minsup = self.minsup

        frequent_itemsets = self.frequent_itemsets = []
        candidates, positions = self._get_initial_candidates_and_positions()
        self.ranges = {}
        self.ranges[ 0 ] = positions

        k = 1
        while True:
            frequent_itemsets.append({})

            for candidate in candidates:
                for (seq_id, sequence) in enumerate(self.sequences):
                    if candidate.issubset(set(sequence)):
                        seq_ids = frequent_itemsets[ k - 1 ].get(candidate, [])
                        if seq_id not in seq_ids:
                            seq_ids.append(seq_id)
                            frequent_itemsets[ k - 1 ][ candidate ] = seq_ids

            frequent_itemsets[ k - 1 ] = { k: v for k, v in frequent_itemsets[ k - 1 ].items() if len(v) >= minsup }

            if len(frequent_itemsets[ k - 1 ]) == 0:
                break

            candidates = []
            for itemset_a, _ in frequent_itemsets[ k - 1 ].items():
                for itemset_b, _ in frequent_itemsets[ k - 1 ].items():
                    combined = itemset_a.union(itemset_b)
                    if len(combined) == len(itemset_a) + 1:
                        candidates.append(combined)
                        self._calculate_ranges(itemset_a, itemset_b, k)
            k = k + 1
        return (k, frequent_itemsets)

    def _calculate_ranges(self, itemset_a, itemset_b, k):
        combined = itemset_a.union(itemset_b)

        sequence_ranges = self.ranges[ k - 1 ]
        result_sequence_ranges = self.ranges.get(k, {})
        for (seq_id, sequence_range) in sequence_ranges.items():
            new_sequence_range = result_sequence_ranges.get(seq_id, {})
            ranges_a = sequence_range.get(itemset_a, [])
            ranges_b = sequence_range.get(itemset_b, [])
            for range_a in ranges_a:
                for range_b in ranges_b:
                    new_range = (min(range_a[ 0 ], range_b[ 0 ]), max(range_a[ 1 ], range_b[ 1 ]))
                    ranges = new_sequence_range.get(combined, [])
                    if new_range not in ranges:
                        ranges.append(new_range)
                        new_sequence_range[ combined ] = ranges

            result_sequence_ranges[ seq_id ] = new_sequence_range
        self.ranges[ k ] = result_sequence_ranges

    def _get_initial_candidates_and_positions(self):
        candidates = []
        positions = {}
        for (seq_id, sequence) in enumerate(self.sequences):
            seq_positions = {}
            for (pos, item) in enumerate(sequence):
                item = frozenset([ item ])
                seq_item_positions = seq_positions.get(item, [])
                seq_item_positions.append((pos, pos))
                seq_positions[ item ] = seq_item_positions
                if item not in candidates:
                    candidates.append(item)
            positions[ seq_id ] = seq_positions
        return (candidates, positions)

    def _find_minimum_window_size(self, itemset, length, seq_id):
        ranges = self.ranges[ length ][ seq_id ][ itemset ]
        min_size = float('inf')
        min_window_size = None
        min_range = None

        for x, y in ranges:
            seq = self.sequences[ seq_id ][ x:y + 1]
            outliers = list(filter(lambda a: a not in itemset, seq))
            size = len(outliers)
            if size < min_size or size == min_size and len(seq) < min_window_size:
                min_size = size
                min_range = (x, y)
                min_window_size = len(seq)
        return (min_size, min_range)

    def _find_epsilon_resilient_itemsets(self, k, itemsets):
        epsilon_resilient_itemsets = {}
        for length in range(k):
            for (itemset, sequences) in itemsets[ length ].items():
                resilient_count = 0
                for seq_id in sequences:
                    outlier_count, min_range = self._find_minimum_window_size(itemset, length, seq_id)
                    # seq = self.sequences[ seq_id ][ min_range[ 0 ]:min_range[ 1 ] + 1 ]
                    if outlier_count / (length + 1) <= self.epsilon:
                        resilient_count += 1
                    # print('seq_id', seq_id, itemset, seq, outlier_count)
                if resilient_count > self.minsup:
                    epsilon_resilient_itemsets[ itemset ] = resilient_count
        return epsilon_resilient_itemsets

    """
    itemsets: array of frozensets
    """
    def _create_output(self, itemsets):
        with open(self.output_filepath, 'w') as f:
            for itemset in itemsets:
                f.write(', '.join(sorted(itemset)))
                f.write('\n')
