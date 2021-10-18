

#ifndef _LITHEALG
#include<bits/stdc++.h>
using namespace std;
#endif

// https://www.hackerearth.com/practice/notes/disjoint-set-union-union-find/
// https://codeforces.com/edu/courses -> in i union find
struct union_find {
 
	vector<int> component_size;
	vector<int> repr;
	
    vector<pair<int,int>> additionalInfo; /* it is possible to maintain sum,min or max of component - in general any associative and commutative function. */
 
	union_find(int number_of_elements) {
		/* Initializing representatives - OBS! starting from 0 */
		for(int i = 0; i < number_of_elements; i++) {
			repr.push_back(i);
			component_size.push_back(1);
			additionalInfo.push_back({ i,i }); /* self is max and min initially */
		}
	}

	int size(int a) {
		/* Returns the size of component which contains node 'a' */
		a = find(a); //det är repr som innehåller all info! - hitta repr!
		return component_size[a];
	}
 
	int find(int a) {
		/* Find representative to 'a' and update transitivity in the go. (Pathcompression - faster runtime next call) */
 
		if (repr[a] == a) {
			return a;
		}
 
		/* Repeat search until 'x' is pointing to 'x' - set every traversed node's immediate repr to x */
		repr[a] = find(repr[a]);

		return repr[a];
	}
 
	void merge(int gravity, int pebble) {
		/* Merges two components given any two nodes */
        /* The core idea of UF is to only adjust repr of each component */
		
		gravity = find(gravity);
		pebble = find(pebble);
 
		/* If they are already in the same component do nothing */
		if (gravity == pebble) {
			return;
		}
 
		/* *Size heuristic* - We always want a smaller size component to merge into a greater size*/
		if (component_size[pebble] > component_size[gravity]) {
			swap(pebble, gravity);
		}

        /* The merge step */
		repr[pebble] = gravity; 
		component_size[gravity] += component_size[pebble];
		component_size[pebble] = 0; 
        

		/* Additional info merge step*/
		additionalInfo[gravity].first = min(additionalInfo[gravity].first, additionalInfo[pebble].first);
		additionalInfo[gravity].second = max(additionalInfo[gravity].second, additionalInfo[pebble].second);

		return;
	}
 
	int count_islands() {
		/* Count number of disjoint components by counting number of non-zero sizes.*/
		int count = 0;
		for (auto el : component_size) {
			if (el > 0) {
				count += 1;
			}
		}
		return count;
	}
    
    /* Common usage is to check if a cycle is created with get*/
	bool get(int u, int v) {
		/* Check if two elements u and v belong to the same set.*/
		u = find(u);
		v = find(v);
		if (u == v) {
			return true;
		}
		return false;
	}
};