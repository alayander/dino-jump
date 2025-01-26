#ifndef SPRITES_HPP
#define SPRITES_HPP

#include "constants.hpp"

#include <array>

extern const std::array<std::array<int, CACTUS_WIDTH>, CACTUS_HEIGHT> SMALL_CACTUS_SPRITE;
extern const std::array<std::array<int, CACTUS_WIDTH>, CACTUS_HEIGHT> LARGE_CACTUS_SPRITE;
extern const std::array<std::array<int, BIRD_WIDTH>, BIRD_HEIGHT> BIRD_SPRITE;
extern const std::array<std::array<int, DINO_WIDTH>, DINO_HEIGHT> DINO_JUMP_SPRITE;
extern const std::array<std::array<int, DINO_WIDTH>, DINO_HEIGHT> DINO_LEFT_SPRITE;
extern const std::array<std::array<int, DINO_WIDTH>, DINO_HEIGHT> DINO_RIGHT_SPRITE;
extern const std::array<std::array<int, DINO_WIDTH>, DINO_HEIGHT> DINO_LEFT_DUCK_SPRITE;
extern const std::array<std::array<int, DINO_WIDTH>, DINO_HEIGHT> DINO_RIGHT_DUCK_SPRITE;
extern const std::array<std::array<int, DEAD_EYE_DIAMETER>, DEAD_EYE_DIAMETER> DEAD_EYE_SPRITE;

#endif // SPRITES_HPP
