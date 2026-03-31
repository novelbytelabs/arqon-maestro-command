# Command Lane Architecture

The command lane is isolated from dictation and other lanes via canonical routing.
Dictation traffic is blocked from command execution paths and records provenance
on every lane decision.

Machine paths enforce protobuf-only protocol handling for infrastructure traffic.
