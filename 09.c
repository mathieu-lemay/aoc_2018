#include <stdio.h>
#include <stdlib.h>

struct marble {
    size_t next;
    size_t prev;
};

typedef struct marble marble_s;

long get_high_score(int nb_players, int last_marble) {
    marble_s *marbles = calloc((last_marble + 1), sizeof(marble_s));
    marble_s marble;
    size_t current = 0;

    long *scores = calloc(nb_players, sizeof(long));

    int p = 0;

    for (long v=1; v<=last_marble; v++) {
        if (v % 23 == 0) {
            for (int i=0; i<7; i++) {
                current = marbles[current].prev;
            }

            scores[p] += (v + current);

            marble = marbles[current];
            marbles[marble.prev].next = marble.next;
            marbles[marble.next].prev = marble.prev;
            current = marble.next;
        } else {
            size_t lhs = marbles[current].next;
            size_t rhs = marbles[lhs].next;

            marbles[lhs].next = v;
            marbles[rhs].prev = v;
            marbles[v].prev = lhs;
            marbles[v].next = rhs;
            current = v;
        }

        p += 1;

        if (p == nb_players) {
            p = 0;
        }
    }

    long hs = 0;
    for (int i=0; i<nb_players; i++) {
        if (scores[i] > hs) {
            hs = scores[i];
        }
    }

    free(marbles);
    free(scores);

    return hs;
}

int main(void) {
    printf("Part 1: %ld\n", get_high_score(458, 72019));
    printf("Part 2: %ld\n", get_high_score(458, 7201900));
}
