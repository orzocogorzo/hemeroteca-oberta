const articlesTable = new DataTable("#articles", {
  language: {
    lengthMenu: "Mosta _MENU_ files per pàgina",
    zeroRecords: "No s'han trobar resultats",
    info: "Pàgina _PAGE_ de _PAGES_",
    infoEmpty: "No hi ha dades",
    infoFiltered: "(filtrades d'un total de _MAX_ files)",
    search: "Cerca: ",
    paginate: {
      first: "Primera",
      last: "Última",
      next: "Següent",
      previous: "Anterior",
    },
  },
  ajax: {
    url: "/hemeroteca/api/articles/?limit=50",
    dataSrc: "",
  },
  columns: [
    {
      data: "title",
      render: (data, _, row) => {
        return `<a href="${row.pk}/">${data}</a>`;
      },
    },
    {
      data: (row) => row.signature?.name,
      render: (data, _, row) => {
        return data !== void 0
          ? `<a href="../signatures/${row.signature.pk}/">${row.signature.name}</a>`
          : "";
      },
    },
    {
      data: (row) => row.section?.name,
      render: (data, _, row) => {
        return data !== void 0
          ? `<a href="../sections/${row.section.pk}">${data}</a>`
          : "";
      },
    },
    {
      data: "publication.number",
      render: (data, _, row) => {
        return `<a href="../publications/${row.publication.pk}/">${data}</a>`;
      },
    },
  ],
});

fetch("/hemeroteca/api/articles/", {
  headers: {
    "Accept": "application/json",
  },
})
  .then((res) => res.json())
  .then((data) => {
    articlesTable.clear();
    articlesTable.rows.add(data).draw();
  });
