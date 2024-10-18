# LinkPty

LinkPty is a Python package that allows you to manage pseudo terminals via WebSocket. It supports creating, managing, and interacting with terminals remotely through a transition Server.

## Installation

To install the package:

```bash
pip install link_pty
```

## Usage
After installing, you can run the terminal manager with:

```bash
link-pty --base-url "your_base_url_here"
```

If no base URL is provided, it defaults to `linkpty.codesocean.top:43143`.

Then you can visit your terminal through `http://{your_base_url_here}/static/index.html`,
it defaults to `http://linkpty.codesocean.top:43143/static/index.html`

## Contribution

Contributions to LinkPty are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository: Start by forking the main repository to your GitHub account.

2. Clone your fork: Clone the forked repository to your local machine.

```bash
git clone https://github.com/your-username/linkpty.git
```

```bash
git checkout -b my-feature-branch
```

3. Make your changes: Add your code or documentation improvements.

4. Commit your changes: Commit your changes with clear and descriptive messages:

```bash
git commit -m "Add feature: describe your feature here"
```

```bash
git push origin my-feature-branch
```

5. Submit a pull request: Navigate to the original repository on GitHub and submit a pull request.

## Issues and Support
If you encounter any bugs or issues, please open an issue in the GitHub Issues section. Be sure to provide detailed information, including steps to reproduce the problem.

For any questions or support, feel free to reach out via the issue tracker or start a discussion on the repository.

## License
LinkPty is licensed under the MIT License. See the LICENSE file for more information.