import { useEffect, useState } from "react";

import SearchInput from "./SearchInput";
import SearchMatches from "./SearchMatches";

import "./style.css";

function SearchControl({ ready, searcher, keyword }) {
  const { Search, highlight } = searcher;

  const [matches, setMatches] = useState([]);
  const [currentMatch, setCurrentMatch] = useState(0);

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
          const onSelectMatch = (match, index) => {
            props.jumpToMatch(index + 1);
            setCurrentMatch(index);
          };

          const jumpToNearest = (dir) => {
            const index = (currentMatch + dir) % props.numberOfMatches;
            setCurrentMatch(index < 0 ? props.numberOfMatches + index : index);
            if (dir > 0) props.jumpToNextMatch();
            else props.jumpToPreviousMatch();
          };

          return (
            <>
              <SearchInput
                {...props}
                setMatches={setMatches}
                jumpPrevious={() => jumpToNearest(-1)}
                jumpNext={() => jumpToNearest(1)}
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
