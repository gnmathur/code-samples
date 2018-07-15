/*
 * The MIT License (MIT)
 * 
 * Copyright (c) [2018] [Gaurav Mathur]
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <cstdint>
#include <iostream>
#include <set>
#include <fstream>
#include <algorithm>

using coordinates_t     = std::pair<int, int>;
using set_of_strings_t  = std::set<std::string>;

class Grid 
{
    public:
        // CTOR
        explicit Grid(uint8_t X, uint8_t Y):
            X_(Y), Y_(Y)
        {
            // Create the grid data-structure and init its contents
            arr_ = new char(X_*Y_);
            for (auto xidx = 0; xidx < X_; xidx++) {
                for (auto yidx = 0; yidx < Y_; yidx++) {
                    *(arr_+(xidx*yidx)+xidx) = 0;
                }
            }
        }
    
        // DTOR
        ~Grid()
        {
            delete[] arr_;
        }
        
        // Delete all other constructors and assignment operators
        Grid(const Grid& rhs)           = delete;
        Grid& operator=(const Grid&)    = delete; 
        Grid(const Grid&&)              = delete;
        Grid& operator=(const Grid&&)   = delete; 
    
        // Define call operator - get
        char operator() (uint8_t x, uint8_t y) const
        {
            return *(arr_+(y*X_)+x);
        }

        // Define call operator - set
        void operator() (uint8_t x, uint8_t y, char val)
        {
            *(arr_+(y*X_)+x) = val;
        }

        /*
         * This routine returns the grid dimensions
         */
        coordinates_t dimensions(void) const
        {
            return coordinates_t(X_, Y_);
        }

        /* Dump the grid to console */
        void dump(void) const
        {
            for (auto yidx = 0; yidx < Y_; yidx++) {
                for (auto xidx = 0; xidx < X_; xidx++) {
                    std::cout << *(arr_+(yidx*X_)+xidx) << " ";
                }
                std::cout  << "\n";
            }
        }

    private:
        // Maximum dimension of X axis
        uint8_t X_;
        // Maximum dimension of Y axis
        uint8_t Y_;
        // Memory region to store the grid
        char    *arr_;
};

class BoggleSolver
{
    public:
        // CTOR
        BoggleSolver(const Grid& G, const set_of_strings_t& dict):
            G_(G), dict_(dict)
        {
            X_ = G.dimensions().first;
            Y_ = G.dimensions().second;

            for (auto word: dict_) {
                for (auto offset = 1; offset <= word.size(); offset++) {
                    prefix_dict_.insert(word.substr(0, offset));
                }
            }
        }

        // Solution algorithm entry point
        set_of_strings_t solve(int x, int y)
        {
            set_of_strings_t result;
            std::string word;
            _solve(result, word, x, y);
            return result;
        }

    private:
        // Core solution logic using backtracking.
        void _solve(set_of_strings_t& result, std::string& word, int x, int y)
        {
            if (x < 0 || y < 0)     { return; }
            if (x >= X_ || y >= Y_)   { return; }

            coordinates_t coor(x, y);

            if (visited_.find(coor) != visited_.end()) { return; }

            // Fetch the character at (x, y) in the grid and append it to the
            // word being built;
            word.push_back(G_(x, y));

            if (prefix_dict_.find(word) == prefix_dict_.end()) { 
                word.pop_back(); 
                return; 
            }

            visited_.insert(coor);

            if (dict_.find(word) != dict_.end()) { 
                result.insert(word);
            }

            /* x-1,y-1 x,y-1 x+1,y-1
             * x-1,y   x,y   x+1,y
             * x-1,y+1,x,y+1 x+1,y+1
             */
            _solve(result, word, x-1, y-1);
            _solve(result, word, x-1, y);
            _solve(result, word, x-1, y+1);
            _solve(result, word, x,   y-1);
            _solve(result, word, x,   y+1);
            _solve(result, word, x+1, y-1);
            _solve(result, word, x+1, y);
            _solve(result, word, x+1, y+1);

            word.pop_back();

            visited_.erase(coor);
        }

    private:
        int                     X_;
        int                     Y_;
        const Grid&             G_;
        const set_of_strings_t& dict_;
        set_of_strings_t        prefix_dict_;
        std::set<coordinates_t> visited_;
};

void test_case2(void)
{
    /*   0 1 2 3
     * 0 d g h i
     * 1 
     * 2 d r l s
     * 3 s e p o
     */
    Grid G(4, 4);
    G(0, 0, 's');
    G(1, 0, 't');
    G(2, 0, 'n');
    G(3, 0, 'g');
    G(0, 1, 'e');
    G(1, 1, 'i');
    G(2, 1, 'a');
    G(3, 1, 'e');
    G(0, 2, 'd');
    G(1, 2, 'r');
    G(2, 2, 'l');
    G(3, 2, 's');
    G(0, 3, 's');
    G(1, 3, 'e');
    G(2, 3, 'p');
    G(3, 3, 'o');

    G.dump();

    set_of_strings_t dict;
    std::ifstream dict_file("dict.txt");
    std::string dict_word;
    while (dict_file >> dict_word) {
        dict.insert(dict_word);
    }

    set_of_strings_t answer;
    for (auto xi = 0; xi < 4; xi++) {
        for (auto yi = 0; yi < 4; yi++) {
            auto result = BoggleSolver(G, dict).solve(xi, yi);
            answer.insert(result.begin(), result.end());
        }
    }
    for (auto word: answer) {
        std::cout << word << " ";
    }
    std::cout << "\n";
}

/*
 * Find words in the grid - 
 *
 *    0 1 2 3
 *    _______
 * 0 |s t n g
 * 1 |e i a e
 * 2 |d r l s
 * 3 |s e p o
 */
set_of_strings_t test_case1(void)
{
    Grid G(4, 4);
    G(0, 0, 's');
    G(1, 0, 't');
    G(2, 0, 'n');
    G(3, 0, 'g');
    G(0, 1, 'e');
    G(1, 1, 'i');
    G(2, 1, 'a');
    G(3, 1, 'e');
    G(0, 2, 'd');
    G(1, 2, 'r');
    G(2, 2, 'l');
    G(3, 2, 's');
    G(0, 3, 's');
    G(1, 3, 'e');
    G(2, 3, 'p');
    G(3, 3, 'o');

    G.dump();

    // Set of dictionary words
    set_of_strings_t   dict;
    // File to read the dictionary words from
    std::ifstream           dict_file("dict.txt");
    // Temporary for holding a parsed dictionary word
    std::string             dict_word;

    // Helper function to give lower case letter for an 
    // upper case ASCII character
    auto lower_case_fn = [](char ch) -> char { 
                            if (ch >= 'A' && ch <= 'Z') 
                                return ch-'A'+'a';
                            else 
                                return ch; 
                            };
                            
    // Read the dictionary line-by-line and extract words
    while (dict_file >> dict_word) {
        // Temporary to hold the lower-case word
        std::string lc_dict_word(dict_word.size(), '\0');
        // Convert parsed word into lower-case
        std::transform(dict_word.begin(), dict_word.end(), lc_dict_word.begin(), 
                lower_case_fn);
        // Add lower-case word to dictionary
        dict.insert(lc_dict_word);
    }

    // Set to store all found words
    set_of_strings_t answer;
    // With each character in the grid as a starting point, find words that 
    // are in the dictionary
    for (auto xi = 0; xi < 4; xi++) {
        for (auto yi = 0; yi < 4; yi++) {
            // Core solver
            auto result = BoggleSolver(G, dict).solve(xi, yi);
            // Add the set of results in our answer set
            answer.insert(result.begin(), result.end());
        }
    }

    return answer;
}

int main(void)
{
    auto answer = test_case1();

    // Print answer
    for (auto word: answer) {
        std::cout << word << " ";
    }

    std::cout << "\n";
    std::cout << "Done.\n";
}

