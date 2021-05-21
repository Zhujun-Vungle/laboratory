# Insomnia
Vungle OLAP solution scripts and configs.
The Insomnia contains the scripts for OLAP solutions.



## Structure

        Insomnia
            ├── production
            |     └── EMR_VERSION1
            |          ├──README.md
            |          └──script1
            |
            |
            ├── experimental
            |     └── EMR_VERSION2
            |           ├──README.md
            |           └──script2   
            |
            |
            ├── README.md



## Setup

| Scripts                  | How to use                 | Location   |
| ------------------------ | -------------------------- | -------------------------- |
| AWS EMR v6.0.0 blueprint | [Instruction](production/EMR_v6.0.0/README.md#how-to-use) | [Script](production/EMR_v6.0.0/generate_blueprint.sh)   |
| .......                  |                           |            |

## Code style

The scripts in this repo should pass the shellcheck https://www.shellcheck.net/.

