import { useEffect, useState } from "react";

function SearchInput({
  keyword,
  setKeyword,
  search,
  jumpPrevious,
  jumpNext,
  setMatches,
  numberOfMatches,
  currentMatch,
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
    if (keyword) search().then((matches) => setMatches(matches));
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
