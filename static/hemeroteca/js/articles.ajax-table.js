const articlesTable = new DataTable("#articles", {
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
  ajax: {
    url: "/hemeroteca/api/articles/",
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
      data: "publication.number",
      render: (data, _, row) => {
        return `<a href="../publications/${row.publication.pk}/">${data}</a>`;
      },
    },
    {
      data: "publication.date",
      render: (data, _, row) => {
        const date = new Date(data);
        let day = date.getDay().toString();
        if (day.length === 1) day = "0" + day;
        let month = (date.getMonth() + 1).toString();
        if (month.length === 1) month = "0" + month;
        const year = date.getFullYear();
        const fmtDate = `${day}-${month}-${year}`;
        return `<a href="../publications/${row.publication.pk}/">${fmtDate}</a>`;
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
  ],
});
