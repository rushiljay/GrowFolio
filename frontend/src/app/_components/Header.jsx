import React from 'react'
import { Button } from '@/components/ui/Button';
import {Accounts} from './Accounts';  

function Header() {

    const accounts = [
        { value: '1', label: 'Account A' },
        { value: '2', label: 'Account B' },
        { value: '3', label: 'Account C' },
    ];
    
return (
    <nav className="flex items-center justify-between px-10 py-8">
        <div className='w-1/4'>
            <Button variant="noHover" className=" h-12 px-6 bg-[#F9B325] font-bold text-2xl animate-none disabled:pointer-events-none text-white drop-shadow-xl" href="/">
                GrowFolio
            </Button>
        </div>
        <div>
            <Accounts accounts={accounts}/> {/** Fix this **/}
        </div>
        <div className="text-black w-1/4 text-right">Icon Placeholder</div>
    </nav>
)
}

export default Header