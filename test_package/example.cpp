#include <cstdint>
#include <type_traits>

int main() {
  enum class A : uint8_t {
    A1,
    A2
  };
  static_assert(std::is_same<std::underlying_type<A>::type, uint8_t>::value);

  int i = 0;
  while(true) ++i;
  return 0;
}
