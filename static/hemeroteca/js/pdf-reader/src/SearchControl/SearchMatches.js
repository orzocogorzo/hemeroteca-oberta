function ellipseText({ pageText, startIndex, endIndex }) {
  const wordsBefore = pageText.substr(startIndex - 20, 20);
  let words = wordsBefore.split(" ");
  words.shift();
  const begin = words.length === 0 ? wordsBefore : words.join(" ");

  const wordsAfter = pageText.substr(endIndex, 60);
  words = wordsAfter.split(" ");
  words.pop();
  const end = words.length === 0 ? wordsAfter : words.join(" ");

  return { pre: begin, match: pageText.substring(startIndex, endIndex), post: end };
}

function SearchMatch({ isCurrent, match, onSelect }) {
  const classList = ["search-match"];
  if (isCurrent) classList.push("current");
  const fmtd = ellipseText(match);
  return (
    <li className={classList.join(" ")} onClick={() => onSelect(match)}>
      {fmtd.pre}
      <span>{fmtd.match}</span>
      {fmtd.post}
    </li>
  );
}

function SearchMatches({ matches, currentIndex, onSelectMatch }) {
  return (
    <ul className="search-matches">
      {(matches.length &&
        matches.map((match, i) => (
          <SearchMatch
            key={i}
            isCurrent={currentIndex === i}
            match={match}
            onSelect={(match) => onSelectMatch(match, i)}
          />
        ))) || (
        <li
          style={{
            textAlign: "center",
            marginTop: "1em",
            opacity: 0.6,
          }}
        >
          Sense resultats
        </li>
      )}
    </ul>
  );
}

export default SearchMatches;
