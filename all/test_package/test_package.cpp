#include "matchmaking_proxy/logic/rating.hxx"
#include <cassert>

int main() {
  assert(matchmaking_proxy::averageRating(10,5) == 2);
  return 0;
}
