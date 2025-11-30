import { Link } from 'react-router-dom';

function MenuButton({icon, caption, to}) {
    return (
        <Link className="flex flex-col justify-center items-center p-3 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500" to={to}>
            <span>{icon}</span>
            <span>{caption}</span>
        </Link>
    )
}

export default function Menu() {
    return (
        <div className='flex flex-col w-full items-center gap-3  border-green-300 mt-3'>
            <div className='flex text-xs gap-3 flex-wrap border-white justify-center'>
                <MenuButton icon="💸" caption="Add transaction" to="/new" />
                <MenuButton icon="💵" caption="Dashboard" to="/" />
                <MenuButton icon="🤑" caption="Transactions" to="/transactions" />
            </div>
      </div>
    )
}