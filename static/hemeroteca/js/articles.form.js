fetch("/archive/api/publications/")
  .then((res) => res.json())
  .then((data) => {
    document.getElementById("publication").innerHTML = data.reduce(
      (html, publication) => {
        return html + `<option value="${publication.id}">${publication.number}</option>`;
      },
      ""
    );
  });
