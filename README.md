# ipynb-to-pdf-bot

Upload a Jupyter notebook **via GitHub issue** → get PDF in `uploads/` automatically.

---

## How to convert

1. Open a **new issue**
2. **Drag & drop** your `.ipynb` file into the description box  
   (GitHub will upload it)
3. Add the label **`convert`**
4. Wait ~30 s – a PDF appears in `uploads/` and the issue is closed with a download link.

Only users listed in the workflow are allowed; repo admins can add more usernames there.

---

## Where is my file?

After the bot finishes, click the link posted in the issue or browse  
`uploads/&lt;your-file&gt;.pdf` in this repository.

---

## Local test (optional)

```bash
pip install nbconvert
jupyter nbconvert notebook.ipynb --to pdf
