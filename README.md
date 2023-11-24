# NBAStats-FlaskWebApp

This Python project utilizes Flask, a web framework, to create a dynamic web application that displays NBA player statistics. The app provides an interactive and user-friendly interface to explore comprehensive statistics for NBA players, including their performance metrics, game averages, and career highlights.

## Features

- **User Authentication:** Allow users to sign up and sign in to access personalized features.

- **Player Statistics:** Display detailed statistics for NBA players, including per-game averages, game logs, and career averages.

- **Team Information:** Explore information about NBA teams, including roster details.

- **League Standings:** View current NBA league standings and conference standings.

- **Interactive UI:** Provide an intuitive and visually appealing interface for users to navigate and explore NBA data.

## Getting Started

### Prerequisites

- Python 3.x
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/NBAStats-FlaskWebApp.git
    cd NBAStats-FlaskWebApp
    ```

2. **Create a virtual environment:**

    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Usage

1. **Run the application:**

    ```bash
    flask run
    ```

2. **Open your web browser and go to [http://localhost:5000](http://localhost:5000).**

3. **Explore the NBA player statistics, team information, and more.**

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, please open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
