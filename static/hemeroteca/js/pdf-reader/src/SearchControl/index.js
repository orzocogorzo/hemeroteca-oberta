import { useEffect, useState } from "react";

import SearchInput from "./SearchInput";
import SearchMatches from "./SearchMatches";

import "./style.css";

function SearchControl({ pk, ready, plugin, keyword, isVector, jumpToPage }) {
  const { Search, highlight } = plugin;

  const [matches, setMatches] = useState([]);
  const [currentMatch, setCurrentMatch] = useState(0);

  useEffect(() => {
    if (matches.length === 0) return;
    setCurrentMatch(0);
    jumpToPage(matches[0].pageIndex - 1);
  }, [matches]);

  useEffect(() => {
    if (!(keyword && ready)) return;
    highlight({
      keyword,
      matchCase: false,
    });
  }, [ready, keyword]);

  return (
    <div className="search-control">
      <Search>
        {(props) => {
          const jumpToMatch = (match, index) => {
            props.jumpToMatch(index + 1);
            setCurrentMatch(index);
            if (!isVector) {
              jumpToPage(match.pageIndex - 1);
            }
          };

          const onSelectMatch = (match, index) => {
            jumpToMatch(match, index);
          };

          const jumpToNearest = (dir) => {
            let index = (currentMatch + dir) % matches.length;
            index = index < 0 ? matches.length + index : index;
            const match = matches[index];
            jumpToMatch(match, index);
          };

          return (
            <>
              <SearchInput
                {...props}
                setMatches={setMatches}
                jumpPrevious={() => jumpToNearest(-1)}
                jumpNext={() => jumpToNearest(1)}
                isVector={isVector}
                pk={pk}
              />
              <SearchMatches
                currentIndex={currentMatch}
                matches={matches}
                onSelectMatch={onSelectMatch}
              />
            </>
          );
        }}
      </Search>
    </div>
  );
}

export default SearchControl;
