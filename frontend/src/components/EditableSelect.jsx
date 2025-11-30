import { useState, useMemo, useRef, useEffect } from "react";

export default function EditableSelect({
  options,
  value,
  onChange,
  onCreate,
  placeholder,
}) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const containerRef = useRef(null);

  const filtered = useMemo(() => {
    return options.filter((c) =>
      c.toLowerCase().includes(search.toLowerCase())
    );
  }, [options, search]);

  const showCreate =
    search.trim() !== "" &&
    !options.some((c) => c.toLowerCase() === search.toLowerCase());

  // Close dropdown if clicked outside
  useEffect(() => {
    const handler = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleSelect = (c) => {
    console.log('handle select')
    onChange(c);
    setSearch("");
    setOpen(false);
  };

  const handleCreate = () => {
    onCreate(search);
    onChange(search);
    setSearch("");
    setOpen(false);
  };

  return (
    <div className="relative" ref={containerRef}>
      <div
        className="border rounded-3xl px-3 py-2 cursor-pointer bg-white"
        onClick={() => setOpen((s) => !s)}
      >
        {value || placeholder}
      </div>

      {open && (
        <div className="absolute left-0 right-0 mt-1 bg-white border rounded-lg shadow-md max-h-60 overflow-auto z-50">
          {/* Search input */}
          <div className="p-2 border-b">
            <input
              type="text"
              className="w-full px-2 py-1 border rounded-md focus:outline-none"
              placeholder={placeholder}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              autoFocus
            />
          </div>

          {/* Existing options */}
          <ul className="max-h-48 overflow-y-auto">
            {filtered.map((c) => (
              <li
                key={c}
                className="px-3 py-2 cursor-pointer hover:bg-gray-100"
                onClick={() => handleSelect(c)}
              >
                {c}
              </li>
            ))}

            {/* Create option */}
            {showCreate && (
              <li
                className="px-3 py-2 cursor-pointer bg-blue-50 hover:bg-blue-100 text-blue-600"
                onClick={handleCreate}
              >
                {search}
              </li>
            )}

            {/* Empty result (no matches and nothing typed) */}
            {!filtered.length && !showCreate && (
              <li className="px-3 py-2 text-gray-400">No options</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
