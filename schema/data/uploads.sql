INSERT INTO uploads
    (user_id, name, slug, creation_time)
VALUES
    (1, 'pset1', '6c67b081ebea4b97b8ab747cfa37eb9', 1407385222975)
;

INSERT INTO upload_files
    (upload_id, filename, contents)
VALUES
    (1, 'hello.c', "// Tommy MacWilliam, 2009\n\n#include <stdio.h>\n\nint main(int argc, char** argv)\n{\n    printf(\"hello, world!\\n\");\n}"),
    (1, 'mario.c', "// Tommy MacWilliam, 2009\n\n#include <stdio.h>\n#include <stdlib.h>\n#include <cs50.h>\n\n// width of terminal window\n#define X_SIZE 80\n// height of terminal window\n#define Y_SIZE 23\n// gap size of 1 creates 2 pixel gap between pyramids\n#define GAP_SIZE 1\n\nvoid construct_pyramid (char pyramid[X_SIZE][Y_SIZE], int);\nvoid print_pyramid (char pyramid[X_SIZE][Y_SIZE]);\n\nint main (int argc, char* argv[])\n{\n    // get user input\n    printf(\"Enter an integer between 1 and 23: \");\n    int height = GetInt();\n\n    // make sure height is between 1 and 23\n    while (height > 23 || height < 1)\n    {\n        printf(\"Enter an integer between 1 and 23: \");\n        height = GetInt();\n    }\n\n    // create 2d array of correct size to hold pyramid data\n    char pyramid[X_SIZE][Y_SIZE];\n\n    // add data to array\n    construct_pyramid(pyramid, height);\n    // loop through pyramid array and output data\n    print_pyramid(pyramid);\n}\n\n/**\n * Construct pyramid by insterting * into array where appropriate.\n * @param pyramid char array containing pyramid data\n * @param height desired height of pyramid\n */\nvoid construct_pyramid (char pyramid[X_SIZE][Y_SIZE], int height)\n{\n    // fill pyramid with spaces to start\n    for (int x = 0; x < X_SIZE; x++)\n    {\n        for (int y = 0; y < Y_SIZE; y++)\n        {\n            pyramid[x][y] = ' ';\n        }\n    }\n\n    // construct right pyramid.\n    // one iteration for each level of the pyramid\n    for (int i = 0; i < height; i++)\n    {\n        // subtract 1 from size to avoid bounds error.\n        // subtracting i moves right to left through the array, constructing\n        // the rightmost piece of each level.\n        pyramid[X_SIZE - 1 - i][Y_SIZE - 1 - i] = '*';\n\n        // fill in rest of level\n        for (int j = 0; j < height - i; j++)\n        {\n            // stay on same level (y-coordinate), but continue to move\n            // right to left through the array in the x by subtracting j.\n            // the intersection of height and i represents the leftmost\n            // part of the right pyramid at the current level.\n            pyramid[X_SIZE - 1 - i - j][Y_SIZE - 1 - i] = '*';\n        }\n    }\n\n    // construct left pyramid.\n    // one iteration for each level of pyramid\n    for (int i = 0; i < height; i++)\n    {\n        // subtract 1 from size to avoid bounds error.\n        // subtract gap size and height twice to shift left pyramid over.\n        // adding i moves left to right through the array, constructing\n        // the leftmost piece of each level.\n        pyramid[X_SIZE - 1 - (2 * height) - GAP_SIZE + i]\n            [Y_SIZE - 1 - i] = '*';\n\n        // fill in rest of level\n        for (int j = 0; j < height - i; j++)\n        {\n            // stay on same level (y-coordinate) but continue to move\n            // left to right through the array in the x by adding j.\n            // subtract gap size and height twice to shift left pyramid over.\n            // intersection of height and i represents the rightmost\n            // part of the left pyramid at the current level.\n            pyramid[X_SIZE - 1 - (2 * height) - GAP_SIZE + i + j]\n                [Y_SIZE - 1 - i] = '*';\n        }\n    }\n}\n\n/**\n * Display pyramid by looping through pyramid array\n * @param pyramid char array containing pyramid data\n */\nvoid print_pyramid (char pyramid[X_SIZE][Y_SIZE])\n{\n    for (int y = 0; y < Y_SIZE; y++)\n    {\n        for (int x = 0; x < X_SIZE; x++)\n        {\n            // display character (either * or space)\n            printf(\"%c\", pyramid[x][y]);\n        }\n        // display newline after every row\n        printf(\"\\n\");\n    }\n}\n")
;
