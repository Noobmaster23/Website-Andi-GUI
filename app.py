import tkinter as tk
from git import Repo

window = tk.Tk()
window.title("Change pictures on heebphotography.ch")
window.configure(width=500, height=300)
window.configure(bg="lightgray")

# testing git
repo_dir = "Website-Andi"
repo = Repo(repo_dir)
# file_list = [
#     'numerical_analysis/regression_analysis/simple_regression_analysis.py',
#     'numerical_analysis/regression_analysis/simple_regression_analysis.png'
# ]
commit_message = 'changed pictures (App)'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()

message = "test"
testing_git = tk.Text(window)
testing_git.insert(tk.INSERT, message)
testing_git.pack()

window.mainloop()
