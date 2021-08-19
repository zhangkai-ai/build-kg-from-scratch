#!usr/bin/python
# -*- coding: utf-8 -*-

import marisa_trie


class TrieTree(object):
    def __init__(self, keys=''):
        if keys:
            self.trie_tree = marisa_trie.Trie(keys)
        else:
            self.trie_tree = marisa_trie.Trie()

    def load(self, persis_path):
        self.trie_tree.load(persis_path)

    def trie_match(self, sent):
        """
        Find all matches in the sent against the trie tree
        :param sent: The input unicode sentence string which is not segmented
        :return: {"key1":[u"match1", u"match2"], "key2":[u"match3", u"match4"], ...}
        """
        # sent must be unicode
        if isinstance(sent, str):
            # sent = sent.decode("utf-8")
            sent = sent

        matched_set = set()
        index = 0
        while index < len(sent):
            matched_list = self.trie_tree.prefixes(sent[index:])
            if matched_list:
                for matched_word in matched_list:
                    matched_set.add(matched_word)
                index += 1
                # max_matched_word = ''
                # for matched_word in matched_list:
                #     if len(matched_word) >= len(max_matched_word):
                #         max_matched_word = matched_word
                # if max_matched_word:
                #     matched_set.add(max_matched_word)
                #     index += len(max_matched_word)
                # else:
                #     index += 1
            else:
                index += 1
        matched_list = sorted(list(matched_set), key=lambda matched_word: len(matched_word), reverse=True)
        return matched_list
