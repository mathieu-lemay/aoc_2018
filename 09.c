#include <stdio.h>
#include <stdlib.h>

struct marble {
    long val;
    struct marble *next;
    struct marble *prev;
};

typedef struct marble marble_s;

long get_high_score(int nb_players, int num_marbles) {
    int c = 0;
    marble_s *marbles = malloc(sizeof(marble_s) * num_marbles);

    marble_s *marble = &marbles[c++];
    marble->val = 0;
    marble->next = marble;
    marble->prev = marble;

    long *scores = calloc(nb_players, sizeof(long));

    int p = 0;

    for (long v=1; v<=num_marbles; v++) {
        if (v % 23 == 0) {
            for (int i=0; i<7; i++) {
                marble = marble->prev;
            }

            scores[p] += (v + marble->val);

            marble_s *prev = marble->prev;
            marble_s *next = marble->next;

            prev->next = next;
            next->prev = prev;
            marble = next;
        } else {
            marble = marble->next->next;

            marble_s *prev = marble->prev;

            marble_s *new_m = &marbles[c++];
            new_m->val = v;
            new_m->prev = prev;
            new_m->next = marble;

            prev->next = new_m;
            marble->prev = new_m;

            marble = new_m;
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
