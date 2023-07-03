const table = new DataTable("#publications", {
  language: {
    lengthMenu: "Mosta _MENU_ files per pàgina",
    zeroRecords: "No s'han trobar resultats",
    info: "Pàgina _PAGE_ de _PAGES_",
    infoEmpty: "No hi ha dades",
    infoFiltered: "(filtrades d'un total de _MAX_ files)",
    search: "Cerca",
    paginate: {
      first: "Primera",
      last: "Última",
      next: "Següent",
      previous: "Anterior",
    },
  },
  data: [],
  columns: [
    {
      data: "cover",
      render: (data, _, row) => {
        return `<a href="../publications/${row.pk}/"><img src="/static/${data}" loading="lazy" /></a>`;
      },
    },
    {
      data: (row) => row.number,
      render: (data, _, row) => {
        return `<a href="../publications/${row.pk}/">${data}</a>`;
      },
    },
    {
      data: "date",
      render: (data, _, row) => {
        const date = new Date(data);
        let day = date.getDay().toString();
        if (day.length === 1) day = "0" + day;
        let month = (date.getMonth() + 1).toString();
        if (month.length === 1) month = "0" + month;
        const year = date.getFullYear();
        const fmtDate = `${day}-${month}-${year}`;
        return `<a href="../publications/${row.pk}/">${fmtDate}</a>`;
      },
    },
  ],
});

const form = document.getElementById("search");
form.addEventListener("submit", (ev) => {
  ev.preventDefault();
  ev.stopPropagation();

  const searchText = ev.target.querySelector('input[type="text"]').value;
  const endpoint = "/hemeroteca/api/search/?text=" + encodeURIComponent(searchText);
  fetch(endpoint)
    .then((res) => res.json())
    .then((data) => {
      table.clear();
      table.rows.add(data).draw();
      // searchResults.splice(0, searchResults.length);
      // data.forEach((datum) => searchResults.push(datum));
      // table.rows().invalidate().draw();
    });
});
