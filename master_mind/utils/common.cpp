#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using Code = std::vector<int>;
using Hint = std::tuple<int, int>;

void count_hitblow(
      Code &code,
      Code &other_code,
      int &hit,
      int &blow,
      int &num_colors,
      int &num_pins
      )
{
   std::vector<int> a(num_colors, 0);
   std::vector<int> b(num_colors, 0);
   hit = 0;
   blow = 0;
   for( int i = 0; i < num_pins; i++ )
   {
      if( code[i] == other_code[i] )
      {
         hit += 1;
      }
      else
      {
         a[code[i]-1] += 1;
         b[other_code[i]-1] += 1;
      }
   }
   for( int j = 0; j < num_colors; j++ )
   {
      blow += std::min(a[j], b[j]);
   }
}


struct tuple_hash
{
    template <class T1, class T2>
    std::size_t operator() (const std::tuple<T1, T2> &t) const {
        return std::hash<T1>()(std::get<0>(t)) ^ std::hash<T2>()(std::get<1>(t));
    }
};

using Distribution = std::unordered_map<Hint, std::deque<Code>, tuple_hash>;

Distribution calc_dist(
      Code &guess,
      std::vector<Code> &feasible_codes,
      int &num_colors,
      int &num_pins
      )
{
   int hit, blow;
   Distribution dist;
   for( auto &code : feasible_codes )
   {
      count_hitblow(guess, code, hit, blow, num_colors, num_pins);
      dist[std::make_tuple(hit, blow)].push_back(code);
   }
   return dist;
}

PYBIND11_MODULE(cpp_utils, m) {
    m.def("calc_dist", &calc_dist);
}
