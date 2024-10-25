#include<bits/stdc++.h>
using namespace std;


void addEdge(unordered_map<int, vector<int>>& adjList, int u, int v) {
    adjList[u].push_back(v);
}


bool detectCycleUtil(int node, unordered_map<int, vector<int>>& adjList, unordered_set<int>& visited, unordered_set<int>& recStack) {
    if (recStack.find(node) != recStack.end()) {
        cout << "Cycle detected at node T" << node << endl;
        return true;
    }

    if (visited.find(node) != visited.end()) {
        return false;
    }


    visited.insert(node);
    recStack.insert(node);

    for (int neighbor : adjList[node]) {
        if (detectCycleUtil(neighbor, adjList, visited, recStack)) {
            return true;
        }
    }


    recStack.erase(node);
    return false;
}


bool detectCycle(unordered_map<int, vector<int>>& adjList) {
    unordered_set<int> visited;
    unordered_set<int> recStack;


    for (auto& pair : adjList) {
        if (visited.find(pair.first) == visited.end()) {
            if (detectCycleUtil(pair.first, adjList, visited, recStack)) {
                return true;
            }
        }
    }

    return false;
}

void printGraph(unordered_map<int, vector<int>>& adjList) {
    cout << "Precedence Graph (Adjacency List):" << endl;
    for (auto& pair : adjList) {
        cout << "T" << pair.first << " -> ";
        for (int neighbor : pair.second) {
            cout << "T" << neighbor << " ";
        }
        cout << endl;
    }
}


bool isConflictSerializable(const vector<vector<string>>& schedule) {
    unordered_map<int, vector<int>> adjList;
    int numTransactions = schedule.size();
    int numSteps = schedule[0].size();


    for (int i = 0; i < numSteps; ++i) {
        for (int t1 = 0; t1 < numTransactions; ++t1) {
            if (schedule[t1][i] == "-") continue;

            char op1 = schedule[t1][i][0];
            char dataItem1 = schedule[t1][i][2];

            for (int t2 = 0; t2 < numTransactions; ++t2) {
                if (t1 == t2) continue;


                for (int j = i + 1; j < numSteps; ++j) {
                    if (schedule[t2][j] == "-") continue;

                    char op2 = schedule[t2][j][0];
                    char dataItem2 = schedule[t2][j][2];


                    if (dataItem1 == dataItem2) {
                        if ((op1 == 'W' && op2 == 'R') || (op1 == 'R' && op2 == 'W') || (op1 == 'W' && op2 == 'W')) {


                                cout << "Conflict detected: T" << t1 + 1 << " -> T" << t2 + 1 << " for data item " << dataItem1 << endl;
                                addEdge(adjList, t1 + 1, t2 + 1);

                        }
                    }
                }
            }
        }
    }

   // printGraph(adjList);



    bool hasCycle = detectCycle(adjList);
    if (hasCycle) {
        cout << "Cycle detected in the graph. The schedule is NOT conflict serializable." << endl;
    } else {
        cout << "No cycle detected. The schedule is conflict serializable." << endl;
    }

    return !hasCycle;
}

int main() {
    ifstream file("schedule1.txt");
    string line;
    vector<vector<string>> schedule;


    while (getline(file, line)) {
        stringstream ss(line);
        string transaction, operation;
        vector<string> operations;


        ss >> transaction;
        while (ss >> operation) {
            operations.push_back(operation);
        }
        schedule.push_back(operations);
    }

    isConflictSerializable(schedule);

    return 0;
}
