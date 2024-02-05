import { useEffect, useState } from "react";

function storeSearch(keyword) {
  const query = new URLSearchParams(window.location.search);
  query.set("search", keyword);
  const location = window.location.pathname + "?" + query.toString();
  window.history.pushState({ from: window.location.search }, null, location);
}

function ajaxSearch({ pk, keyword }) {
  const endpoint =
    process.env.REACT_APP_SITE_URL +
    process.env.REACT_APP_API_URL +
    `matches/${pk}?pattern=${encodeURIComponent(keyword)}`;
  return fetch(endpoint, {
    method: "GET",
    headers: {
      "Accept": "application/json; charset=utf-8",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      let lastPage,
        matchIndex = 0;
      return data.matches.map((match, i) => {
        if (lastPage === match.pageIndex) {
          matchIndex += 1;
        } else {
          matchIndex = 0;
        }
        return {
          "keyword": new RegExp(keyword, "gi"),
          "matchIndex": matchIndex,
          "pageIndex": match.pageIndex,
          "pageText": match.pageText,
          "startIndex": match.startIndex,
          "endIndex": match.endIndex,
        };
      });
    });
}

function SearchInput({
  keyword,
  setKeyword,
  search,
  jumpPrevious,
  jumpNext,
  setMatches,
  numberOfMatches,
  currentMatch,
  isVector,
  pk,
}) {
  const [value, setValue] = useState(keyword ? keyword : "");

  const onKeyDown = (ev) => {
    if (ev.keyCode !== 13) return;
    setKeyword(value);
  };

  const onChange = (ev) => {
    setValue(ev.target.value);
    if (ev.nativeEvent.type === "input") return;
    setKeyword(ev.target.value);
  };

  useEffect(() => {
    if (!keyword) return;
    if (isVector) {
      search(keyword).then((matches) => {
        setMatches(matches);
      });
    } else {
      ajaxSearch({ pk, keyword }).then((matches) => {
        setMatches(matches);
      });
    }
    storeSearch(keyword);
  }, [keyword]);

  return (
    <div className="search-actions">
      <div className="search-input">
        <label>
          Cerca:
          <input type="text" value={value} onKeyDown={onKeyDown} onChange={onChange} />
        </label>
      </div>
      <nav className="search-nav">
        <button onClick={jumpPrevious}>
          <svg
            aria-hidden="true"
            className="rpv-core__icon"
            focusable="false"
            height="16px"
            viewBox="0 0 24 24"
            width="16px"
          >
            <path
              d="M23.535,18.373L12.409,5.8c-0.183-0.207-0.499-0.226-0.706-0.043C11.688,5.77,11.674,5.785,11.66,5.8
            L0.535,18.373"
            ></path>
          </svg>
        </button>
        <button onClick={jumpNext}>
          <svg
            aria-hidden="true"
            className="rpv-core__icon"
            focusable="false"
            height="16px"
            viewBox="0 0 24 24"
            width="16px"
          >
            <path
              d="M0.541,5.627L11.666,18.2c0.183,0.207,0.499,0.226,0.706,0.043c0.015-0.014,0.03-0.028,0.043-0.043
            L23.541,5.627"
            ></path>
          </svg>
        </button>
      </nav>
      <div className="search-bookmark">
        <h3>
          Coincidències: {currentMatch}/{numberOfMatches}
        </h3>
      </div>
    </div>
  );
}

export default SearchInput;
